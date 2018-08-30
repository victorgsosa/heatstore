import json
import pika
import logging

from flask_restful import Resource
from services.camera import CameraService
from util.encoder import Encoder

log = logging.getLogger(__name__)

class BaseCameraController(object):

	def __init__(self, camera_service: CameraService):
		self.camera_service = camera_service

	def find_cameras(self, images):
		cameras = {image['camera']: self.camera_service.find_one(image['camera']) for image in images} 
		return cameras


	def send_to_rabbit_for_action(self, channel, images, cameras, queue, action):
		selected_images = [image for image in images if image['camera'] in cameras.keys() and cameras[image['camera']].has_action(action)]
		if selected_images:
			log.debug('Sending images for action %s in queue %s', action, queue)
			channel.queue_declare(queue=queue, durable=True)
			channel.basic_publish(exchange='',
					routing_key=queue,
	                body=json.dumps(selected_images, cls=Encoder),
	                properties=pika.BasicProperties(
	                delivery_mode = 2, # make message persistent
	                ))

	def send_to_rabbit_for_role(self, channel, images, cameras, role):
		selected_images = [image for image in images if image['camera'] in cameras.keys() and cameras[image['camera']].has_role(role)]
		if selected_images:
			log.debug('Sending images for role %s to the exchange', role)
			channel.exchange_declare(exchange=role,
				exchange_type='fanout')
			channel.basic_publish(exchange=role,
							routing_key='',
		                    body=json.dumps(selected_images, cls=Encoder),
		                    properties=pika.BasicProperties(
		                    delivery_mode = 2, # make message persistent
		                          ))