import uuid
import cv2
import time
import pika 
import json
import numpy as np
import logging
import util.images as im

from flask import request, current_app as app
from flask_restful import Resource
from PIL import Image
from services.image_detector.person_detector import PersonDetector
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
	
	def __init__(self, detector: PersonDetector, camera_service: CameraService, connection: pika.BlockingConnection = None):
		BaseCameraController.__init__(self, camera_service)
		self.detector = detector
		self.connection = connection

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
		log.debug("Processing %i images", len(images))
		detections = self.detect_persons(images)
		log.debug("Added detections %s", detections)
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
		detections = self.detector.detect([im.read_base64(image['content']) for image in images], 0.90)
		return detections

	def send_to_rabbit(self, images, cameras):
		if self.connection:
			channel = self.connection.channel()
			super(ImageDetectorController, self).send_to_rabbit_for_action(channel, images, cameras, self.LOCATION_QUEUE, self.LOCATION_ACTION)
			super(ImageDetectorController, self).send_to_rabbit_for_action(channel, images, cameras, self.CROP_QUEUE, self.CROP_ACTION)
			


