import logging
import json
import numpy as np
import util.images as im
import cv2

from flask import request, current_app as app
from flask_restful import Resource
from services.camera import CameraService
from services.face_detector.classifiers import AbstractFaceClassifier
from services.face_detector import AlignDlib, default_image_size
from services.amqp import BlockingPublisher
from typing import List, Dict

from api import BaseCameraController

log = logging.getLogger(__name__)

class ClassifierController(BaseCameraController, Resource):
	CLASSIFICATOR_ROLE = 'CLASSIFICATOR'

	def __init__(self, camera_service: CameraService, classifiers: List[Dict[str, AbstractFaceClassifier]], 
		aligner: AlignDlib, publisher: BlockingPublisher, preprocessor = None, threshold = 0.9):
		BaseCameraController.__init__(self, camera_service, publisher)
		self.classifiers = classifiers
		self.aligner = aligner
		self.preprocessor = preprocessor
		self.threshold = threshold

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
		aligned_image = self._align_image(image_cv, default_image_size)
		if aligned_image is  None:
			return {}
		if self.preprocessor is not None:
			aligned_image = self.preprocessor(aligned_image)
		input_image = np.expand_dims(aligned_image,0)
		raw_classes = [(classifier['name'], classifier['model'].predict(input_image)[0], classifier['model'].predict_proba(input_image)[0])
				for classifier in self.classifiers ]
		classes = { name: {
				'value':  clazz,
				'probability': prob
			} for (name, clazz, prob) in raw_classes if prob > self.threshold }  
		return classes

	def _align_image(self, image, crop_dim):
		bb = self.aligner.getLargestFaceBoundingBox(image)
		aligned = self.aligner.align(crop_dim, image, bb, landmarkIndices=AlignDlib.INNER_EYES_AND_BOTTOM_LIP)
		if aligned is not None:
			aligned = cv2.cvtColor(aligned, cv2.COLOR_BGR2RGB)
		return aligned

	def send_to_rabbit(self, images, cameras):
		super(ClassifierController, self).send_to_rabbit_for_role(images, cameras, self.CLASSIFICATOR_ROLE)


