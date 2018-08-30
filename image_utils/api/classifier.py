import logging
import json
import numpy as np
import pika

from flask import request, current_app as app
from flask_restful import Resource
from services.camera import CameraService
from services.face_detector.classifiers import SVMFaceClassifier
from typing import List, Dict

from api import BaseCameraController

log = logging.getLogger(__name__)

class ClassifierController(BaseCameraController, Resource):
	CLASSIFICATOR_ROLE = 'CLASSIFICATOR'

	def __init__(self, camera_service: CameraService, classifiers: List[Dict[str, SVMFaceClassifier]], connection: pika.BlockingConnection = None):
		BaseCameraController.__init__(self, camera_service)
		self.classifiers = classifiers
		self.connection = connection

	def consume(self, channel, method, properties, body):
		images = json.loads(body)
		cameras = super(ClassifierController, self).find_cameras(images)
		images = self.add_classes(images)
		self.send_to_rabbit(images, cameras)


	def post(self):
		images = request.get_json(force=True)
		cameras = super(ClassifierController, self).find_cameras(images)
		images = self.add_classes(images)
		self.send_to_rabbit(images)
		return images

	def add_classes(self, images):
		log.debug("Classifying images")
		classes = [[self.classify(embeddings) for embeddings in image['embeddings']] for image in images]
		log.debug("Added classification %s", classes)
		for i in range(len(images)):
			images[i]['classes'] = classes[i]
		return images

	def classify(self, embeddings):
		if not embeddings:
			return {}
		classes = dict((classifier['name'], classifier['model'].predict(np.expand_dims(embeddings,0))[0]) for classifier in self.classifiers)
		return classes


	def send_to_rabbit(self, images, cameras):
		if self.connection:
			channel = self.connection.channel()
			super(ClassifierController, self).send_to_rabbit_for_role(channel, images, cameras, self.CLASSIFICATOR_ROLE)


