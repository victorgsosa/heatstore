import numpy as np
import logging

from util.encoder import Encoder

class Config(object):
	MODEL_PATH = 'resources/image_detector/frozen_inference_graph.pb'
	DEBUG = True
	CAMERA_HEIGHT = 2
	CAMERA_FOCAL_LENGTH = 1333.333333
	CAMERA_DISTANCES = np.array([3.33, 3.33, 3.33])
	CAMERA_MEASURES = np.array([[-205.192232,572.27504], [-18.075456,579.67873], [186.132704,574.00758]])
	IMAGE_QUEUE = 'image_queue'
	RESTFUL_JSON = {'cls': Encoder}
	DETECTION_WORKERS = 1
	LOCATION_WORKERS = 1 
	RABBITMQ_HEARTBEAT_INTERVAL = 600
	RABBITMQ_BLOCKED_CONNECTION_TIMEOUT = 300

class DevelopmentConfig(Config):
	PORT = 5000
	RABBITMQ_HOST = 'amqp://localhost:5672'
	LOG_LEVEL = logging.DEBUG


class ProductionConfig(Config):
	PORT = 8080
	RABBITMQ_HOST = 'amqp://rBakm7-46ZLZf6cK:jnHVnendNaspSWXf@10.11.241.11:35617'
	DEBUG = False
	LOG_LEVEL = logging.DEBUG