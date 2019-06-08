import numpy as np
import tensorflow as tf
import cv2

from .abstract_face_classifier import AbstractFaceClassifier

classes_dir = {'(0, 2)': 0, '(15, 25)': 1, '(25, 35)': 2, '(35, 43)': 3, '(2, 8)': 4, '(48, 53)': 5, '(60, 100)': 6, '(8, 15)': 7}

image_size = 160


class ResNetModel(object):
	@staticmethod
	def load_model(path):
		return tf.keras.models.load_model(path)

	def __init__(self, filename):
		self._model = self.load_model(filename)
		self._graph = tf.get_default_graph()

	def predict(self, X):
		with self._graph.as_default():
			return self._model.predict_classes(X)

	def predict_proba(self, X):
		with self._graph.as_default():
			return self._model.predict(X).max(axis=1)

	def save(self, filename):
		pass

class ResNetFaceClassifier(AbstractFaceClassifier):

	def __init__(self, name):
		super().__init__()
		self._name = name
		self._session = tf.Session()

	def _train(self, X, y):
		pass

	def predict(self, X):
		with self._session.as_default():
			return self._model.predict(X)

	def predict_proba(self, X):
		with self._session.as_default():
			return self._model.predict_proba(X)

	def save(self, filename):
		_self._model.save(filename)

	def _change_layer_names(self, model):
		for layer in model.layers:
			layer._name = self._name + '_' + layer._name
			if isinstance(layer, tf.keras.models.Model):
				self._change_layer_names(layer)
				print(layer.summary())
		return model

	def _load(self, filename):
		with self._session.as_default():
			return ResNetModel(filename)

	@staticmethod
	def process_image(image):
		resized_image = cv2.resize(image, (image_size, image_size))
		resized_image = resized_image / 1./255
		resized_image = np.expand_dims(resized_image, 0)
		return resized_image




