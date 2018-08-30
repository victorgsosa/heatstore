import os
import pika
import logging
import sys
import json


from flask import Flask
from flask_restful import Api
from services.image_detector import PersonDetector, PersonDetectorModel
from services.image_locator import ImageLocator
from services.amqp import AMQPConsumerManager
from services.image_cropper import ImageCropper
from services.camera import CameraService
from services.face_detector import AlignDlib, Facenet, FacenetModel
from services.face_detector.classifiers import SVMFaceClassifier
from concurrent.futures import ThreadPoolExecutor
from api import ImageDetectorController, ImageLocatorController, CropperController, EmbeddingsController, ClassifierController
from healthcheck import HealthCheck
from typing import List, Dict
from util.encoder import Encoder


config = {
    "dev": "config.DevelopmentConfig",
    "prod": "config.ProductionConfig"
}

app = Flask(__name__)
api = Api(app)
config_name = os.environ.get('IMAGE_UTILS_ENV', 'dev')
app.config.from_object(config[config_name])
logging.basicConfig(level=app.config['LOG_LEVEL'], stream=sys.stdout)
app.logger.info("Configuring from %s" % config[config_name])
health = HealthCheck(app, "/health")
person_detector = PersonDetector(PersonDetectorModel(path=app.config['PERSON_MODEL_PATH']))
cropper = ImageCropper()
camera_service = CameraService(app.config['CAMERA_SERVICE_URL'])
aligner =  AlignDlib(app.config['FACE_ALIGNER_PATH'])
facenet = Facenet(FacenetModel(app.config['FACE_EMBEDDINGS_PATH']))
gender_classifier = SVMFaceClassifier()
gender_classifier.load(app.config['GENDER_CLASSIFIER_PATH'])
classifiers = [
	{'name': 'gender', 'model': gender_classifier}
]
	


def get_rabbitmq_host(app):
	if 'RABBITMQ_HOST' in app.config:
		return app.config['RABBITMQ_HOST']
	else:
		if 'RABBITMQ_SERVICE' in app.config:
			env_vars = os.getenv('VCAP_SERVICES')
			service = json.loads(env_vars)[app.config['RABBITMQ_SERVICE']][0]
			return service['credentials']['uri']
	return None


def main():
	pika_url = "%s/?socket_timeout=%s&heartbeat_interval=%s&blocked_connection_timeout=%s" % (get_rabbitmq_host(app), app.config['RABBITMQ_SOCKET_TIMEOUT'],app.config['RABBITMQ_HEARTBEAT_INTERVAL'], app.config['RABBITMQ_BLOCKED_CONNECTION_TIMEOUT'])
	app.logger.info('registering consumers...')
	amqp_consumer = AMQPConsumerManager(pika_url)
	amqp_consumer.add_consumer(EmbeddingsController.CLASSIFIER_QUEUE, ClassifierController(camera_service, classifiers, pika.BlockingConnection(pika.URLParameters(pika_url))).consume)
	app.logger.info('Consumer for queue %s added', EmbeddingsController.CLASSIFIER_QUEUE)
	amqp_consumer.add_consumer(CropperController.EMBEDDINGS_QUEUE, EmbeddingsController(camera_service, aligner, facenet, pika.BlockingConnection(pika.URLParameters(pika_url))).consume)
	app.logger.info('Consumer for queue %s added', CropperController.EMBEDDINGS_QUEUE)
	amqp_consumer.add_consumer(ImageDetectorController.LOCATION_QUEUE, ImageLocatorController(camera_service, pika.BlockingConnection(pika.URLParameters(pika_url))).consume)
	app.logger.info('Consumer for queue %s added', ImageDetectorController.LOCATION_QUEUE)
	amqp_consumer.add_consumer(ImageDetectorController.CROP_QUEUE, CropperController(cropper, camera_service, pika.BlockingConnection(pika.URLParameters(pika_url))).consume)
	app.logger.info('Consumer for queue %s added', ImageDetectorController.CROP_QUEUE)
	amqp_consumer.add_consumer(app.config['IMAGE_QUEUE'], ImageDetectorController(person_detector, camera_service, pika.BlockingConnection(pika.URLParameters(pika_url))).consume)
	app.logger.info('Consumer for queue %s added', app.config['IMAGE_QUEUE'])

	api.add_resource(ImageDetectorController, '/detector', resource_class_kwargs={
		'detector': person_detector,
		'camera_service': camera_service,
		'connection': pika.BlockingConnection(pika.URLParameters(pika_url))
		})
	api.add_resource(ImageLocatorController, '/locator', resource_class_kwargs={
		'camera_service': camera_service,
		'connection': pika.BlockingConnection(pika.URLParameters(pika_url))
		})
	api.add_resource(CropperController, '/cropper', resource_class_kwargs={
		'cropper': cropper,
		'camera_service': camera_service,
		'connection': pika.BlockingConnection(pika.URLParameters(pika_url))
		})
	api.add_resource(EmbeddingsController, '/embeddings', resource_class_kwargs={
		'aligner': aligner,
		'facenet': facenet,
		'camera_service': camera_service,
		'connection': pika.BlockingConnection(pika.URLParameters(pika_url))
		})
	api.add_resource(ClassifierController, '/classifier', resource_class_kwargs={
		'classifiers': classifiers,
		'camera_service': camera_service,
		'connection': pika.BlockingConnection(pika.URLParameters(pika_url))
		})

	app.run(host='0.0.0.0', port=app.config['PORT'], debug=app.config['DEBUG'])


def print_locations_callback(ch, method, properties, body):
	images = json.loads(body)
	app.logger.debug("Detections found %s", [image['detections'] for image in images])

if __name__ == '__main__':
	main()






