
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import classification_report
from sklearn.svm import SVC
from sklearn.externals import joblib
from services.face_detector.classifiers.abstract_face_classifier import AbstractFaceClassifier
from sklearn.externals.joblib import parallel_backend
from sklearn import preprocessing


class SVMFaceClassifier(AbstractFaceClassifier):

	def __init__(self):
		super().__init__()
		self._model_class = SVC
		tuned_parameters = [{'kernel': ['rbf'], 'gamma': [1, 1e-1, 1e-2, 1e-3, 1e-4],
			'C': [1, 10, 100, 1000]},
			{'kernel': ['linear'], 'C': [1, 10, 100]}]
		self._model = GridSearchCV(SVC(), tuned_parameters, cv=5, scoring='f1_macro', n_jobs=1, verbose=100)

	def _train(self, X, y):
		self._model.fit(X, y)
		return self._model

	def predict(self, X):
		return self._model.predict(X)

	def predict_proba(self, X):
		return self._model.predict_proba(X)

	def save(self, filename):
		joblib.dump(self._model, filename)

	def _load(self, filename):
		return joblib.load(filename) 

	def _preprocess_X(self, X):
		return preprocessing.scale(X)


