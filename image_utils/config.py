import numpy as np
import logging

from util.encoder import Encoder

class Config(object):
	MODEL_PATH = 'resources/image_detector/frozen_inference_graph.pb'
	DEBUG = True
	CAMERA_HEIGHT = 2
	CAMERA_FOCAL_LENGTH = 1333.333333
	CAMERA_DISTANCES = np.array([3.33, 3.33, 3.33])
	CAMERA_MEASURES = np.array([[-71.73979282,299.4118094], [277.7164698,310.8430266], [-259.8790325,319.5241928]])
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
	RABBITMQ_HOST = 'amqp://ibBXrgPcCawRE5G1:JQf6cfgbqKJSLgaU@10.11.241.9:32771'
	DEBUG = False
	LOG_LEVEL = logging.DEBUG