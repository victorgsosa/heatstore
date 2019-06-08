import logging
import json
import numpy as np

from flask import request, current_app as app
from flask_restful import Resource
from services.camera import CameraService
from services.face_detector.classifiers import AbstractFaceClassifier
from services.amqp import BlockingPublisher
from typing import List, Dict

from api import BaseCameraController

log = logging.getLogger(__name__)

class ClassifierController(BaseCameraController, Resource):
	CLASSIFICATOR_ROLE = 'CLASSIFICATOR'

	def __init__(self, camera_service: CameraService, classifiers: List[Dict[str, AbstractFaceClassifier]], publisher: BlockingPublisher, preprocessor = None):
		BaseCameraController.__init__(self, camera_service, publisher)
		self.classifiers = classifiers
		self.preprocessor = preprocessor

	def consume(self, channel, method, properties, body):
		images = json.loads(body)
		cameras = super(ClassifierController, self).find_cameras(images)
		images = self.add_classes(images)
		self.send_to_rabbit(images, cameras)


	def post(self):
		images = request.get_json(force=True)
		cameras = super(ClassifierController, self).find_cameras(images)
		images = self.add_classes(images)
		self.send_to_rabbit(images, cameras)
		return images

	def add_classes(self, images):
		log.info("Classifying images")
		classes = [[self.classify(embeddings) for embeddings in image['crops']] for image in images]
		log.info("Added classification %s", classes)
		for i in range(len(images)):
			images[i]['classes'] = classes[i]
		return images

	def classify(self, image):
		image_cv = im.base64_to_cv(image)
		if self.preprocessor is not None:
			image_cv = self.preprocessor(image_cv)
		classes = dict((classifier['name'], classifier['model'].predict(np.expand_dims(image_cv,0))[0]) for classifier in self.classifiers)
		return classes


	def send_to_rabbit(self, images, cameras):
		super(ClassifierController, self).send_to_rabbit_for_role(images, cameras, self.CLASSIFICATOR_ROLE)


