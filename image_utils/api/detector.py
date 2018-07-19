import uuid
import cv2
import time
import pika 
import json
import numpy as np
import logging
import util.images as im

from flask import request, current_app as app
from flask_injector import inject
from flask_restful import Resource
from PIL import Image
from services.image_detector.person_detector import PersonDetector
from concurrent.futures import ThreadPoolExecutor
from util.encoder import Encoder


log = logging.getLogger(__name__)

class ImageDetectorService(Resource):
	DETECTION_QUEUE = 'detection_queue'
	
	@inject
	def __init__(self, detector: PersonDetector, connection: pika.BlockingConnection = None):
		self.detector = detector
		self.connection = connection

	def consume(self, channel, method, properties, body):
		images = json.loads(body)
		images = self.add_detections(images)
		self.send_to_rabbit(images)


	def post(self):
		images = request.get_json(force=True)
		images = self.add_detections(images)
		self.send_to_rabbit(images)
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
		detections = self.detector.detect([im.read_base64(image['content']) for image in images], 0.8)
		return detections

	def send_to_rabbit(self, detections):
		if self.connection:
			channel = self.connection.channel()
			channel.queue_declare(queue=self.DETECTION_QUEUE, durable=True)
			channel.basic_publish(exchange='',
					routing_key='detection_queue',
                    body=json.dumps(detections, cls=Encoder),
                    properties=pika.BasicProperties(
                    delivery_mode = 2, # make message persistent
                          ))



