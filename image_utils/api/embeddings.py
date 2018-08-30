import logging
import json
import util.images as im
import pika
import cv2

from flask import request, current_app as app
from flask_restful import Resource
from services.face_detector import AlignDlib, Facenet, default_image_size
from services.camera import CameraService

from api import BaseCameraController

log = logging.getLogger(__name__)

class EmbeddingsController(BaseCameraController, Resource):
	CLASSIFIER_QUEUE = 'classifier'
	CLASSIFIER_ACTION = 'CLASSIFY'
	COUNTER_IN_ROLE = 'COUNTER_IN'
	COUNTER_OUT_ROLE = 'COUNTER_OUT'

	def __init__(self, camera_service: CameraService, aligner: AlignDlib, facenet: Facenet, connection: pika.BlockingConnection = None):
		BaseCameraController.__init__(self, camera_service)
		self.aligner = aligner
		self.facenet = facenet
		self.connection = connection

	def consume(self, channel, method, properties, body):
		images = json.loads(body)
		cameras = super(EmbeddingsController, self).find_cameras(images)
		images = self.add_embeddings(images)
		self.send_to_rabbit(images, cameras)

	def post(self):
		images = request.get_json(force=True)
		cameras = super(EmbeddingsController, self).find_cameras(images)
		images = self.add_embeddings(images)
		self.send_to_rabbit(images, cameras)
		return images

	def add_embeddings(self, images):
		log.debug("Adding embeddings to images")
		embeddings = [[self.embeddings(crop)  for crop in image['crops']] for image in images]
		log.debug("Added embeddings %s", embeddings)
		for i in range(len(images)):
			images[i]['embeddings'] = embeddings[i]
		return images

	def embeddings(self, image):
		image_cv = im.base64_to_cv(image)
		aligned_image = self._align_image(image_cv, default_image_size)
		if aligned_image is  None:
			return []
		embeddings = self.facenet.detect([im.cv_to_byte_string(aligned_image)])[0]
		return embeddings


	def _align_image(self, image, crop_dim):
		bb = self.aligner.getLargestFaceBoundingBox(image)
		aligned = self.aligner.align(crop_dim, image, bb, landmarkIndices=AlignDlib.INNER_EYES_AND_BOTTOM_LIP)
		if aligned is not None:
			aligned = cv2.cvtColor(aligned, cv2.COLOR_BGR2RGB)
		return aligned

	def send_to_rabbit(self, images, cameras):
		print(self.connection)
		if self.connection:
			channel = self.connection.channel()
			super(EmbeddingsController, self).send_to_rabbit_for_action(channel, images, cameras, self.CLASSIFIER_QUEUE, self.CLASSIFIER_ACTION)
			super(EmbeddingsController, self).send_to_rabbit_for_role(channel, images, cameras, self.COUNTER_IN_ROLE)
			super(EmbeddingsController, self).send_to_rabbit_for_role(channel, images, cameras, self.COUNTER_OUT_ROLE)

