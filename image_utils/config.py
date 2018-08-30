import numpy as np
import logging

from util.encoder import Encoder

class Config(object):
	DEBUG = True
	IMAGE_QUEUE = 'images'
	RESTFUL_JSON = {'cls': Encoder}
	DETECTION_WORKERS = 1
	LOCATION_WORKERS = 1 
	RABBITMQ_SOCKET_TIMEOUT = 600
	RABBITMQ_HEARTBEAT_INTERVAL = 0
	RABBITMQ_BLOCKED_CONNECTION_TIMEOUT = 300
	CAMERA_SERVICE_URL = "https://heatstoreapis0018881710trial.hanatrial.ondemand.com/heatstore-api/cameras"
	PERSON_MODEL_PATH = 'resources/image_detector/frozen_inference_graph.pb'
	FACE_ALIGNER_PATH = 'resources/face_detection/shape_predictor_68_face_landmarks.dat' 
	FACE_EMBEDDINGS_PATH =  'resources/face_detection/frozen_facenet.pb'
	GENDER_CLASSIFIER_PATH = 'resources/face_detection/gender.pkl'


class DevelopmentConfig(Config):
	PORT = 5000
	RABBITMQ_HOST = 'amqp://localhost:5672'
	LOG_LEVEL = logging.DEBUG


class ProductionConfig(Config):
	PORT = 8080
	RABBITMQ_HOST = 'amqp://guest:guest@172.31.32.133:5672'
	DEBUG = False
	LOG_LEVEL = logging.DEBUG
	CAMERA_SERVICE_URL = "https://heatstoreapis0018881710trial.hanatrial.ondemand.com/heatstore-api/cameras"
	PERSON_MODEL_PATH = '/usr/local/share/heatstore/resources/image_detector/frozen_inference_graph.pb'
	FACE_ALIGNER_PATH = '/usr/local/share/heatstore/resources/face_detection/shape_predictor_68_face_landmarks.dat' 
	FACE_EMBEDDINGS_PATH =  '/usr/local/share/heatstore/resourcesface_detection/frozen_facenet.pb'
	GENDER_CLASSIFIER_PATH = '/usr/local/share/heatstore/resources/face_detection/gender.pkl'