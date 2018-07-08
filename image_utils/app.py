import os
import pika
import logging
import sys
import json


from injector import Binder
from flask import Flask
from flask_injector import FlaskInjector
from flask_restful import Api
from services.image_detector.person_detector import PersonDetector, PersonDetectorModel
from services.image_locator.image_locator import ImageLocator, ImageLocatorCalibrator
from services.amqp.amqp_consumer_manager import AMQPConsumerManager
from concurrent.futures import ThreadPoolExecutor
from api.detector import ImageDetectorService
from api.locator import ImageLocatorService
from model.camera import Camera
from healthcheck import HealthCheck
from util.encoder import Encoder


config = {
    "dev": "config.DevelopmentConfig",
    "prod": "config.ProductionConfig"
}

app = Flask(__name__)
api = Api(app)
config_name = os.getenv('IMAGE_UTILS_ENV', 'dev')
app.config.from_object(config[config_name])
logging.basicConfig(level=app.config['LOG_LEVEL'], stream=sys.stdout)
pika_connection = pika.BlockingConnection(pika.URLParameters(app.config['RABBITMQ_HOST']))
image_locator= ImageLocator(ImageLocatorCalibrator(
				camera = Camera(app.config['CAMERA_FOCAL_LENGTH'], app.config['CAMERA_HEIGHT']),
				measures = {
					'distances': app.config['CAMERA_DISTANCES'],
					'values': app.config['CAMERA_MEASURES']
				}
			))
person_detector = PersonDetector(PersonDetectorModel(path=app.config['MODEL_PATH']))

amqp_consumer = AMQPConsumerManager(app.config['RABBITMQ_HOST'])


def configure(binder: Binder) -> Binder:
	binder.bind(
		PersonDetector,
		person_detector
	)
	binder.bind(
		ThreadPoolExecutor,
		ThreadPoolExecutor(max_workers=10)
	)
	binder.bind(
		pika.BlockingConnection,
		pika_connection
		)
	binder.bind(
		ImageLocator,
		image_locator
		)


def print_locations_callback(ch, method, properties, body):
	images = json.loads(body)
	app.logger.debug("Locations found %s", [image['locations'] for image in images])

if __name__ == '__main__':
	api.add_resource(ImageDetectorService, '/detector')
	api.add_resource(ImageLocatorService, '/locator')
	FlaskInjector(app=app, modules=[configure])

	health = HealthCheck(app, "/health")
	app.logger.info('registering consumers...')
	amqp_consumer.add_consumer(ImageDetectorService.DETECTION_QUEUE, ImageLocatorService(image_locator, pika_connection).consume)
	app.logger.info('Consumer for queue %s added', ImageDetectorService.DETECTION_QUEUE)
	amqp_consumer.add_consumer(app.config['IMAGE_QUEUE'], ImageDetectorService(person_detector, pika_connection).consume)
	amqp_consumer.subscribe(ImageLocatorService.LOCATION_EXCHANGE, print_locations_callback)
	app.logger.info('Consumer for queue %s added', app.config['IMAGE_QUEUE'])
	app.run(host='0.0.0.0', port=app.config['PORT'], debug=app.config['DEBUG'])






