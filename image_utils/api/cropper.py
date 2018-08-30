import logging
import json
import util.images as im
import pika

from flask import request, current_app as app
from flask_restful import Resource
from services.image_cropper import ImageCropper
from services.camera import CameraService

from api import BaseCameraController

log = logging.getLogger(__name__)

class CropperController(Resource, BaseCameraController):
	EMBEDDINGS_QUEUE = 'embeddings'
	EMBEDDINGS_ACTION = 'EMBEDDINGS'

	def __init__(self, cropper: ImageCropper, camera_service: CameraService, connection: pika.BlockingConnection = None):
		BaseCameraController.__init__(self, camera_service)
		self.cropper = cropper
		self.connection = connection

	def consume(self, channel, method, properties, body):
		images = json.loads(body)
		cameras = super(CropperController, self).find_cameras(images)
		images = self.add_crops(images)
		self.send_to_rabbit(images, cameras)


	def post(self):
		images = request.get_json(force=True)
		cameras = super(CropperController, self).find_cameras(images)
		images = self.add_crops(images)
		self.send_to_rabbit(images, cameras)
		return images

	def add_crops(self, images):
		log.debug("Cropping images")
		crops = [self.crop_image(image['content'], image['detections']) for image in images]
		log.debug("Added crops %s", crops)
		for i in range(len(images)):
			images[i]['crops'] = [ im.to_base64(crop) for crop in crops[i] ]
		return images


	def crop_image(self, image, detections):
		return self.cropper.crop(im.read_base64(image), detections)

	def send_to_rabbit(self, images, cameras):
		if self.connection:
			channel = self.connection.channel()
			super(CropperController, self).send_to_rabbit_for_action(channel, images, cameras, self.EMBEDDINGS_QUEUE, self.EMBEDDINGS_ACTION)		
