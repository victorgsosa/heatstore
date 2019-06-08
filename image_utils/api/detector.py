import uuid
import cv2
import time
import json
import numpy as np
import logging
import util.images as im

from flask import request, current_app as app
from flask_restful import Resource
from PIL import Image
from services.image_detector.person_detector import PersonDetector
from services.amqp import BlockingPublisher
from concurrent.futures import ThreadPoolExecutor
from services.camera import CameraService
from util.encoder import Encoder
from api import BaseCameraController


log = logging.getLogger(__name__)

class ImageDetectorController(Resource, BaseCameraController):
	LOCATION_QUEUE = 'locations'
	CROP_QUEUE = 'crops'
	LOCATION_ACTION = 'LOCATION'
	CROP_ACTION = 'CROP'
	
	def __init__(self, detector: PersonDetector, camera_service: CameraService, publisher: BlockingPublisher):
		BaseCameraController.__init__(self, camera_service, publisher)
		self.detector = detector

	def consume(self, channel, method, properties, body):
		images = json.loads(body)
		cameras = super(ImageDetectorController, self).find_cameras(images)
		images = self.add_detections(images)
		self.send_to_rabbit(images, cameras)


	def post(self):
		images = request.get_json(force=True)
		cameras = super(ImageDetectorController, self).find_cameras(images)
		images = self.add_detections(images)
		self.send_to_rabbit(images, cameras)
		return images

	def add_detections(self, images):
		log.info("Processing %i images", len(images))
		detections = self.detect_persons(images)
		log.info("Added detections %s", detections)
		for i in range(len(images)):
			width, height = im.image_size(im.read_base64(images[i]['content']))
			images[i]['detections'] = [{
				'score': detection['score'],
				'xMin': detection['xMin'] * width,
				'yMin': detection['yMin'] * height,
				'xMax': detection['xMax'] * width,
				'yMax': detection['yMax'] * height,
			} for detection in detections[i]]
		return images

	def detect_persons(self, images):
		#TODO: Threshold 
		detections = self.detector.detect([im.read_base64(image['content']) for image in images], 0.8)
		return detections

	def send_to_rabbit(self, images, cameras):
		super(ImageDetectorController, self).send_to_rabbit_for_action(images, cameras, self.LOCATION_QUEUE, self.LOCATION_ACTION)
		super(ImageDetectorController, self).send_to_rabbit_for_action(images, cameras, self.CROP_QUEUE, self.CROP_ACTION)
			


