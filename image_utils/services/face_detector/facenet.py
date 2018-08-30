import numpy as np
import tensorflow as tf

from util.decorators import lazy_property, timing


default_image_size = 160

class FacenetModel(object):

	def __init__(self, path):
		self.path = path
		self.detector 
		self.graph
		self.image_input 
		self.image_tensor


	@lazy_property
	def graph(self):
		graph = tf.Graph()
		with tf.gfile.Open(self.path, 'rb') as graph_def_file:
			graph_content = graph_def_file.read()
		graph_def = tf.GraphDef()
		graph_def.ParseFromString(graph_content)
		with graph.as_default():
			tf.import_graph_def(
				graph_def, name='', input_map={'input': self.image_tensor, 
				'phase_train': tf.convert_to_tensor(False)})
		return graph

	@lazy_property
	def image_input(self):
		image = tf.placeholder(dtype=tf.string, name="image")
		return image

	@lazy_property
	def image_tensor(self):
		decoded_image_tensor = tf.image.decode_image(self.image_input, channels=3)
		float_image_tensor = tf.image.convert_image_dtype(decoded_image_tensor, tf.float32)
		float_image_tensor.set_shape([default_image_size, default_image_size, 3])
		image_tensor = tf.expand_dims(float_image_tensor, 0)
		return image_tensor

	@lazy_property
	def detector(self):
		embedding_layer = tf.squeeze(
			self.graph.get_tensor_by_name("embeddings:0")
			)

		return embedding_layer

class Facenet(object):
	def __init__(self, model: FacenetModel):
		self.model = model
		self.sess = tf.Session()

	@timing
	def detect(self, images):
		graph = self.model.graph
		with tf.Session(graph=graph) as sess:
			images_dataset = tf.data.Dataset.from_tensor_slices(images)
			iterator = tf.data.Iterator.from_structure(images_dataset.output_types,
			images_dataset.output_shapes)
			image_batch = iterator.get_next()
			embeddings = []
			it_init = iterator.make_initializer(images_dataset)
			init_op = tf.group(tf.global_variables_initializer(), tf.local_variables_initializer())
			sess.run(init_op)
			sess.run(it_init)
			while True:
				try:
					image = sess.run(image_batch)
					embedding = sess.run( self.model.detector,
		 				feed_dict = {self.model.image_input: image})
					embeddings.append(embedding)
				except tf.errors.OutOfRangeError:
					tf.logging.info('Finished processing records')
					break
		return embeddings
			

