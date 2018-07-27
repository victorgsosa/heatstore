import tensorflow as tf
import util.decorators as decorators


class PersonDetectorModel(object):

	def __init__(self, path):
		self.path = path
		self.graph = tf.Graph()
		tf.logging.debug('Reading graph and building model...')
		self.image_input 
		self.image_tensor
		self.detector 

	@decorators.lazy_property
	def image_input(self):
		with self.graph.as_default():
			image = tf.placeholder(dtype=tf.string, name="image")
		return image

	@decorators.lazy_property
	def image_tensor(self):
		with self.graph.as_default():
			image_tensor = tf.image.decode_image(self.image_input, channels=3, name = "decoder")
			image_tensor.set_shape([None, None, 3])
			image_tensor = tf.expand_dims(image_tensor, 0)
		return image_tensor

	@decorators.lazy_property
	def detector(self):
		with tf.gfile.Open(self.path, 'rb') as graph_def_file:
			graph_content = graph_def_file.read()
		graph_def = tf.GraphDef()
		graph_def.MergeFromString(graph_content)
		with self.graph.as_default():
			tf.import_graph_def(
				graph_def, name='', input_map={'image_tensor': self.image_tensor})

		g = self.graph

		num_detections_tensor = tf.squeeze(
			g.get_tensor_by_name('num_detections:0'), 0)
		num_detections_tensor = tf.cast(num_detections_tensor, tf.int32)

		detected_boxes_tensor = tf.squeeze(
			g.get_tensor_by_name('detection_boxes:0'), 0)
		detected_boxes_tensor = detected_boxes_tensor[:num_detections_tensor]

		detected_scores_tensor = tf.squeeze(
			g.get_tensor_by_name('detection_scores:0'), 0)
		detected_scores_tensor = detected_scores_tensor[:num_detections_tensor]

		detected_labels_tensor = tf.squeeze(
			g.get_tensor_by_name('detection_classes:0'), 0)
		detected_labels_tensor = tf.cast(detected_labels_tensor, tf.int64)
		detected_labels_tensor = detected_labels_tensor[:num_detections_tensor]
		return {
			'detected_boxes_tensor': detected_boxes_tensor, 
			'detected_scores_tensor': detected_scores_tensor, 
			'detected_labels_tensor': detected_labels_tensor
			}
		

class PersonDetector(object):
	def __init__(self, model: PersonDetectorModel):
		self.model = model

	@decorators.timing
	def detect(self, images, threshold = 0.5):
		embeddings = []
		with tf.Session(graph=self.model.graph) as sess:
			sess.run(tf.local_variables_initializer())
			for image in images:
				boxes, scores, classes = self.infer(
				  image)
				imageDetections.append([
			  			{
		   				"score": scores[i],
		  				"xMin" : boxes[1][i],
		   				"yMin" : boxes[0][i],
			 			"xMax" : boxes[3][i],
			 			"yMax" : boxes[2][i]
			  		}
			  		for i in range(len(scores)) if scores[i] > threshold
			  	])

			tf.logging.info('Finished processing records')

		return imageDetections
			

	def infer(self, image):
		(detected_boxes, detected_scores,
			detected_classes) = tf.get_default_session().run([
				self.model.detector['detected_boxes_tensor'], self.model.detector['detected_scores_tensor'],
				self.model.detector['detected_labels_tensor']
			], feed_dict = {self.model.image_input: image})
		detected_boxes = detected_boxes.T
		return detected_boxes, detected_scores, detected_classes


