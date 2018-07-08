import json
import pika
import numpy as np
import uuid
import logging
import util.images as im

from flask import request
from flask_injector import inject
from flask_restful import Resource
from services.image_locator.image_locator import ImageLocator
from model.camera import Camera
from util.encoder import Encoder

log = logging.getLogger(__name__)

class ImageLocatorService(Resource):
	LOCATION_EXCHANGE = 'locations'
	
	@inject
	def __init__(self, locator: ImageLocator, connection: pika.BlockingConnection = None):
		self.locator = locator
		self.connection = connection


	def consume(self, channel, method, properties, body):
		images = json.loads(body)
		images = self.add_locations(images)
		self.send_to_rabbit(images)

	def post(self):
		images = request.get_json(force=True)
		images = self.add_locations(images)
		self.send_to_rabbit(locations)
		return locations

	def add_locations(self, images):
		locations = [ self.locate(image['detections'], im.image_size(im.read_base64(image['content']))[0]) if image['detections'] else [] for image in images]
		log.debug("added locations %s", locations)
		for i in range(len(images)):
			images[i]['locations'] = locations[i]
		return images

	def locate(self, detections, width):
		points = np.array([[(annotation['xMax'] + annotation['xMin'])/ 2 - width / 2, annotation['yMax']] for annotation in detections])
		locations = self.locator.locate(points)
		log.debug("measured %s", locations)
		return [
			{
				'x': point[0],
				'y': point[1]
			} for point in locations
		]

	def image_size(self, image):
		image_np = np.fromstring(image, np.uint8)
		image_decoded = cv2.imdecode(image_np, cv2.IMREAD_COLOR)
		return image_decoded.shape[1], image_decoded.shape[0]

	def send_to_rabbit(self, locations):
		if self.connection:
			channel = self.connection.channel()
			channel.exchange_declare(exchange=self.LOCATION_EXCHANGE,
                         exchange_type='fanout')
			channel.basic_publish(exchange=self.LOCATION_EXCHANGE,
					routing_key='',
                    body=json.dumps(locations, cls=Encoder),
                    properties=pika.BasicProperties(
                    delivery_mode = 2, # make message persistent
                          ))
