import json
import pika
import logging

from flask_restful import Resource
from services.camera import CameraService
from services.amqp import BlockingPublisher
from util.encoder import Encoder

log = logging.getLogger(__name__)

class BaseCameraController(object):

	def __init__(self, camera_service: CameraService, publisher: BlockingPublisher):
		self.camera_service = camera_service
		self.publisher = publisher

	def find_cameras(self, images):
		cameras = {image['camera']: self.camera_service.find_one(image['camera']) for image in images} 
		return cameras


	def send_to_rabbit_for_action(self, images, cameras, queue, action):
		selected_images = [image for image in images 
			if image['camera'] in cameras.keys()
			and cameras[image['camera']].has_action(action)]
		if selected_images:
			log.info('Sending images for action %s in queue %s', action, queue)
			self.publisher.send_to_queue(
				queue, 
				json.dumps(selected_images, cls=Encoder),
				pika.BasicProperties(
		                delivery_mode = 2, # make message persistent
		                ),
				queue)

	def send_to_rabbit_for_role(self, images, cameras, role):
		selected_images = [image for image in images 
			if image['camera'] in cameras.keys() 
			and cameras[image['camera']].has_role(role)]
		if selected_images:
			log.info('Sending images for role %s to the exchange', role)
			self.publisher.send_to_exchange(
				role,
				json.dumps(selected_images, cls=Encoder),
				pika.BasicProperties(
			                    delivery_mode = 2, # make message persistent
			                        ))