import os
import pika
import logging
import sys
import json


from flask import Flask
from flask_restful import Api
from services.image_detector import PersonDetector, PersonDetectorModel
from services.image_locator import ImageLocator
from services.amqp import AMQPConsumerManager, BlockingPublisher
from services.image_cropper import ImageCropper
from services.camera import CameraService
from services.face_detector import AlignDlib, Facenet, FacenetModel
from services.face_detector.classifiers import ResNetFaceClassifier
from concurrent.futures import ThreadPoolExecutor
from api import ImageDetectorController, ImageLocatorController, CropperController, EmbeddingsController, ClassifierController
from healthcheck import HealthCheck
from typing import List, Dict
from util.encoder import Encoder



def get_rabbitmq_host(application):
	if 'RABBITMQ_HOST' in application.config:
		return application.config['RABBITMQ_HOST']
	else:
		if 'RABBITMQ_SERVICE' in application.config:
			env_vars = os.getenv('VCAP_SERVICES')
			service = json.loads(env_vars)[application.config['RABBITMQ_SERVICE']][0]
			return service['credentials']['uri']
	return None


config = {
    "dev": "config.DevelopmentConfig",
    "prod": "config.ProductionConfig"
}


application = Flask(__name__)
api = Api(application)
config_name = os.environ.get('IMAGE_UTILS_ENV', 'dev')
application.config.from_object(config[config_name])
if 'LOG_FILE' in application.config:
	logging.basicConfig(level=application.config['LOG_LEVEL'], filename=application.config['LOG_FILE'], format=application.config['LOG_FORMAT'])
else:
	logging.basicConfig(level=application.config['LOG_LEVEL'], stream=sys.stderr, format=application.config['LOG_FORMAT'])
application.logger.info("Configuring from %s" % config[config_name])
application.logger.info(__name__)
health = HealthCheck(application, "/health")
person_detector = PersonDetector(PersonDetectorModel(path=application.config['PERSON_MODEL_PATH']))
cropper = ImageCropper()
camera_service = CameraService(application.config['CAMERA_SERVICE_URL'])
aligner =  AlignDlib(application.config['FACE_ALIGNER_PATH'])
facenet = Facenet(FacenetModel(application.config['FACE_EMBEDDINGS_PATH']))
gender_classifier = ResNetFaceClassifier('gender', binary=True)
gender_classifier.load(application.config['GENDER_CLASSIFIER_PATH'])
age_classifier = ResNetFaceClassifier('age')
age_classifier.load(application.config['AGE_CLASSIFIER_PATH'])
classifiers = [
	{'name': 'gender', 'model': gender_classifier},
	{'name': 'age', 'model': age_classifier}
]
amqp_url = "%s/?socket_timeout=%s&heartbeat_interval=%s&blocked_connection_timeout=%s" % (
	get_rabbitmq_host(application), 
	application.config['RABBITMQ_SOCKET_TIMEOUT'],
	application.config['RABBITMQ_HEARTBEAT_INTERVAL'],
	application.config['RABBITMQ_BLOCKED_CONNECTION_TIMEOUT'])

application.logger.info('registering consumers...')
amqp_consumer = AMQPConsumerManager(amqp_url)
amqp_consumer.add_consumer(EmbeddingsController.CLASSIFIER_QUEUE, 
	ClassifierController(camera_service, classifiers, aligner, BlockingPublisher(amqp_url), ResNetFaceClassifier.process_image, application.config['CLASSIFICATION_THRESHOLD']).consume)
application.logger.info('Consumer for queue %s added', EmbeddingsController.CLASSIFIER_QUEUE)
amqp_consumer.add_consumer(CropperController.EMBEDDINGS_QUEUE, EmbeddingsController(camera_service, aligner, facenet, BlockingPublisher(amqp_url)).consume)
application.logger.info('Consumer for queue %s added', CropperController.EMBEDDINGS_QUEUE)
amqp_consumer.add_consumer(ImageDetectorController.LOCATION_QUEUE, ImageLocatorController(camera_service, BlockingPublisher(amqp_url)).consume)
application.logger.info('Consumer for queue %s added', ImageDetectorController.LOCATION_QUEUE)
amqp_consumer.add_consumer(ImageDetectorController.CROP_QUEUE, CropperController(cropper, camera_service, BlockingPublisher(amqp_url)).consume)
application.logger.info('Consumer for queue %s added', ImageDetectorController.CROP_QUEUE)
amqp_consumer.add_consumer(application.config['IMAGE_QUEUE'], ImageDetectorController(person_detector, camera_service, BlockingPublisher(amqp_url)).consume, True)
application.logger.info('Consumer for queue %s added', application.config['IMAGE_QUEUE'])
amqp_consumer.start()
api.add_resource(ImageDetectorController, '/detector', resource_class_kwargs={
		'detector': person_detector,
		'camera_service': camera_service,
		'publisher': BlockingPublisher(amqp_url)
		})
api.add_resource(ImageLocatorController, '/locator', resource_class_kwargs={
		'camera_service': camera_service,
		'publisher': BlockingPublisher(amqp_url)
		})
api.add_resource(CropperController, '/cropper', resource_class_kwargs={
		'cropper': cropper,
		'camera_service': camera_service,
		'publisher': BlockingPublisher(amqp_url)
		})
api.add_resource(EmbeddingsController, '/embeddings', resource_class_kwargs={
		'aligner': aligner,
		'facenet': facenet,
		'camera_service': camera_service,
		'publisher': BlockingPublisher(amqp_url)
		})
api.add_resource(ClassifierController, '/classifier', resource_class_kwargs={
		'classifiers': classifiers,
		'camera_service': camera_service,
		'publisher': BlockingPublisher(amqp_url),
		'preprocessor' : ResNetFaceClassifier.process_image
		})
if __name__ == '__main__':
	application.run(host='0.0.0.0', port=application.config['PORT'], debug=application.config['DEBUG'])












