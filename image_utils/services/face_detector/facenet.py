import numpy as np
import tensorflow as tf

from util.decorators import lazy_property, timing


default_image_size = 160

class FacenetModel(object):

	def __init__(self, path):
		self.path = path
		self.detector 
		self.image_input 
		self.image_tensor



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
		with tf.gfile.Open(self.path, 'rb') as graph_def_file:
			graph_content = graph_def_file.read()
		graph_def = tf.GraphDef()
		graph_def.ParseFromString(graph_content)
		results = tf.import_graph_def(
				graph_def, name='', 
				input_map={'input': self.image_tensor, 'phase_train': tf.convert_to_tensor(False)},
				return_elements=["embeddings:0"])
		embedding_layer = tf.squeeze(results[0], 0)

		return embedding_layer

class Facenet(object):
	def __init__(self, model: FacenetModel):
		self.model = model
		self.session = tf.Session()

	@timing
	def detect(self, images):
		embeddings = []
		for image in images:
			embedding = self.session.run( self.model.detector,
		 			feed_dict = {self.model.image_input: image})
			embeddings.append(embedding)
		tf.logging.info('Finished processing records')
		return embeddings
			

