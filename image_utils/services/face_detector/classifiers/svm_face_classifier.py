from sklearn.model_selection import GridSearchCV
from sklearn.metrics import classification_report
from sklearn.svm import SVC
from sklearn.externals import joblib


class SVMFaceClassifier(AbstractFaceClassifier):

	def __init__(self):
		super().__init__(self)
		self._model_class = SVC
		tuned_parameters = [{'kernel': ['rbf'], 'gamma': [1e-3, 1e-4],
                     'C': [1, 10, 100, 1000]},
                    {'kernel': ['linear'], 'C': [1, 10, 100, 1000]}]

        self._model = GridSearchCV(SVC(), tuned_parameters, cv=5,
                       scoring='f1_macro')

		self.scores = ['precision', 'recall']

	def _train(self, X_train, y_train, X_test, y_test):
		self._model.fit(X, y)
		return self._model

	def predict(self, x):
		return self._model.predict(x)

	def save(self, filename):
		joblib.dump(self._model, filename)

	def _load(self, filename):
		return joblib.load('filename.pkl') 


