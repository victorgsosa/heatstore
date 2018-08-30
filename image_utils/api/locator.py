import json
import pika
import numpy as np
import uuid
import logging
import util.images as im

from flask import request
from flask_restful import Resource
from services.image_locator import ImageLocator
from services.camera import CameraService
from model.camera import Camera
from util.encoder import Encoder

from api import BaseCameraController


log = logging.getLogger(__name__)

class ImageLocatorController(BaseCameraController, Resource):
	LOCATION_ROLE = 'LOCATOR'
	
	def __init__(self, camera_service: CameraService, connection: pika.BlockingConnection = None):
		BaseCameraController.__init__(self, camera_service)
		self.connection = connection


	def consume(self, channel, method, properties, body):
		images = json.loads(body)
		cameras = super(ImageLocatorController, self).find_cameras(images)
		images = self.add_locations(images, cameras)
		self.send_to_rabbit(images, cameras)

	def post(self):
		images = request.get_json(force=True)
		cameras = super(ImageLocatorController, self).find_cameras(images)
		images = self.add_locations(images, cameras)
		self.send_to_rabbit(images)
		return images


	def add_locations(self, images, cameras):
		locations = [ self.locate(cameras[image['camera']],image['detections'], im.image_size(im.read_base64(image['content']))[0]) if image['detections'] else [] for image in images]
		log.debug("added locations %s", locations)
		for i in range(len(images)):
			for j in range(len(images[i]['detections'])):
				images[i]['detections'][j]['x'] = locations[i][j]['x']
				images[i]['detections'][j]['y'] = locations[i][j]['y']
		return images

	def locate(self, camera, detections, width):
		points = np.array([[(annotation['xMax'] + annotation['xMin'])/ 2 - width / 2, annotation['yMax']] for annotation in detections])
		locator = ImageLocator()
		locations = locator.locate(camera, points)
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

	def send_to_rabbit(self, images, cameras):
		if self.connection:
			channel = self.connection.channel()
			super(ImageLocatorController, self).send_to_rabbit_for_role(channel, images, cameras, self.LOCATION_ROLE)

