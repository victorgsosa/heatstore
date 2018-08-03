from abc import ABCMeta, abstractmethod
class AbstractFaceClassifier(object):
	__metaclass__ = ABCMeta
	def __init__(self):
		self._model
		self._model_class

	def load(self, filename):
		self._model = self._load(filename)
	@abstractmethod
	def _load(self, filename): raise NotImplementedError()

	
	def train(self, X, y): raise NotImplementedError():
		self._model = self._train(X,y)

	@abstractmethod
	def _train(self, X, y)

	@abstractmethod
	def save(self, filename): raise NotImplementedError()

	@abstractmethod
	def predict(self, x): raise NotImplementedError()





