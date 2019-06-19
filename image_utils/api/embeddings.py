import logging
import json
import util.images as im
import cv2

from flask import request, current_app as app
from flask_restful import Resource
from services.face_detector import AlignDlib, Facenet, default_image_size
from services.amqp import BlockingPublisher
from services.camera import CameraService

from api import BaseCameraController

log = logging.getLogger(__name__)

class EmbeddingsController(BaseCameraController, Resource):
	CLASSIFIER_QUEUE = 'classifier'
	CLASSIFIER_ACTION = 'CLASSIFY'
	COUNTER_IN_ROLE = 'COUNTER_IN'
	COUNTER_OUT_ROLE = 'COUNTER_OUT'

	def __init__(self, camera_service: CameraService, aligner: AlignDlib, facenet: Facenet, publisher: BlockingPublisher):
		BaseCameraController.__init__(self, camera_service, publisher)
		self.aligner = aligner
		self.facenet = facenet

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
		log.info("Adding embeddings to images")
		embeddings = [[self.embeddings(crop)  for crop in image['crops']] for image in images]
		log.info("Added embeddings %s", embeddings)
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
		super(EmbeddingsController, self).send_to_rabbit_for_action(images, cameras, self.CLASSIFIER_QUEUE, self.CLASSIFIER_ACTION)
		super(EmbeddingsController, self).send_to_rabbit_for_role(images, cameras, self.COUNTER_IN_ROLE)
		super(EmbeddingsController, self).send_to_rabbit_for_role(images, cameras, self.COUNTER_OUT_ROLE)

