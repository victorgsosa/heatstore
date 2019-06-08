import tensorflow as tf
import numpy as np

from services.face_detector.classifiers.abstract_face_classifier import AbstractFaceClassifier
from util.decorators import lazy_property

class NNFaceClassifierModel(object):
	def __init__(self, input_dim, num_classes):
		self._input_dim = input_dim
		self._num_classes = num_classes
		self.input
		self.neural_net
		self.classifier
		self.prediction
		self.proba

	@lazy_property
	def input(self):
		return tf.placeholder(tf.float32, [None, self._input_dim], name = "input")


	@lazy_property
	def neural_net(self):
		hidden_num = 512
		w1 = tf.Variable(tf.random_normal([self._input_dim, hidden_num], mean=0, stddev=0.1))
		b1 = tf.Variable(tf.zeros([hidden_num]))
		layer_1 = tf.add(tf.matmul(self.input, w1), b1)
		relu_1 = tf.nn.relu(layer_1)
		w2 = tf.Variable(tf.random_normal([hidden_num, hidden_num], mean=0, stddev=0.1))
		b2 = tf.Variable(tf.zeros([hidden_num]))
		layer_2 = tf.add(tf.matmul(relu_1, w2), b2)
		relu_2 = tf.nn.relu(layer_2)
		wout = tf.Variable(tf.random_normal([hidden_num, self._num_classes], mean=0, stddev=0.1))
		bout = tf.Variable(tf.zeros([self._num_classes]))
		out_layer = tf.add(tf.matmul(relu_2, wout), bout)
		return out_layer

	@lazy_property
	def classifier(self):
		return tf.nn.softmax(self.neural_net, name = "classifier")

	@lazy_property
	def prediction(self):
		return tf.argmax(self.classifier,1, name = "prediction")

	@lazy_property
	def proba(self):
		return tf.reduce_max(self.classifier,1, name = "proba")


class NNFaceClassifier(AbstractFaceClassifier):

	def __init__(self):
		super().__init__()
		self.session = tf.Session()


	def _train(self, X, y):
		numEpochs = 10
		learningRate = 0.001
		input_dim = X.shape[1]
		num_classes = np.amax(y) + 1
		num_classes = np.amax(y) + 1
		features = tf.placeholder(tf.float32, [None, input_dim])
		labels = tf.placeholder(tf.float32, [None])
		dataset = tf.data.Dataset.from_tensor_slices((features, labels))
		batched_dataset = dataset.batch(10)
		iterator = batched_dataset.make_initializable_iterator()
		next_element = iterator.get_next()

		model = NNFaceClassifierModel(input_dim, num_classes)
		y_train = tf.placeholder(tf.int32, [None])
		one_hot = tf.one_hot(y_train, depth = num_classes, dtype = tf.float32)
		one_hot = tf.stop_gradient(one_hot)
		cost_OP = tf.reduce_mean(tf.nn.sparse_softmax_cross_entropy_with_logits(logits = model.classifier, labels = y_train ))
		training_OP = tf.train.AdamOptimizer(learningRate).minimize(cost_OP)

		correct_predictions_OP = tf.equal(model.prediction,tf.argmax(one_hot,1))
		# If every false prediction is 0 and every true prediction is 1, the average returns us the accuracy
		accuracy_OP = tf.reduce_mean(tf.cast(correct_predictions_OP, "float"))
		self.session.run(tf.global_variables_initializer())
		self.session.run(iterator.initializer, feed_dict={features: X,
                                          labels: y})
		cost = 0
		diff = 1
		for  i in range(numEpochs):
			while True:
				# Run training step
				try:
					xBatch , yBatch = self.session.run(next_element)
				except tf.errors.OutOfRangeError:
					break
				step = self.session.run(training_OP, feed_dict={model.input: xBatch, y_train: yBatch})
			
				# Generate accuracy stats on test data
			classifier, train_accuracy, newCost = self.session.run([model.classifier, accuracy_OP, cost_OP], feed_dict={model.input: X, y_train: y})
			# Re-assign values for variables
			print(classifier)
			diff = abs(newCost - cost)
			cost = newCost
			print("epoch %d, training accuracy %g, cost %g, change in cost %g"%(i, train_accuracy, newCost, diff))	

	def predict(self, X):
		graph = tf.get_default_graph()
		classifier = graph.get_tensor_by_name("classifier:0")
		prediction = graph.get_tensor_by_name("prediction:0")
		input = graph.get_tensor_by_name("input_1:0")
		return self.session.run(prediction, feed_dict={input: X})

	def predict_proba(self, X):
		graph = tf.get_default_graph()
		proba = graph.get_tensor_by_name("proba:0")
		input = graph.get_tensor_by_name("input:0")
		return self.session.run(proba, feed_dict={input: X})

	def save(self, filename):
		saver = tf.train.Saver()
		saver.save(self.session, filename)

	def _load(self, filename): 
		saver = tf.train.import_meta_graph(filename)
		saver.restore(self.session, tf.train.latest_checkpoint('./'))
		#print(self.session.graph.get_operations())






