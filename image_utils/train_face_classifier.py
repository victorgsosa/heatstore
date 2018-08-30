import argparse
import numpy as np
import scipy.io

from services.face_detector.classifiers.svm_face_classifier import SVMFaceClassifier


def train(embeddings, classes, output_file):
	classifier = SVMFaceClassifier()
	np.random.seed(0)
	classifier.train(embeddings, classes)
	classifier.save(output_file)

def sample(embeddings, classes, size):
	indexes = np.random.randint(0, embeddings.shape[0], size)
	return embeddings[indexes], classes[indexes]

def main(embeddings_file, meta_filename, y_meta, output_file, ignored_examples_file=None):
	print('Reading embeddings...')
	with open(embeddings_file,'rb') as f:
		embeddings = np.loadtxt(f, delimiter=',', dtype=np.float64)
	print('embeddings readed')
	print('Reading metadata')
	meta = scipy.io.loadmat(meta_filename, squeeze_me=True)['imdb']
	print('Metadata readed')
	length = embeddings.shape[0]
	y = np.array(meta[y_meta].tolist(), dtype=np.float64)
	if ignored_examples_file:
		print('Removing ignored images...')
		with open(ignored_examples_file, 'rb') as f:
			ignored_examples = np.loadtxt(ignored_examples_file, delimiter=',').astype(np.int64)
		length = length + ignored_examples.shape[0]
		y = y[0:length]
		used = np.ones(y.shape[0], dtype=np.int64)
		used[ignored_examples] = 0
		y = np.compress(used, y)
	else:
		y = y[0:length]

	embeddings = embeddings[~np.isnan(y)]
	y = y[~np.isnan(y)]
	embeddings, y = sample(embeddings, y, 20000)
	print('Training with %d images' % embeddings.shape[0])
	train(embeddings, y, output_file)


if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('--embeddings', dest='embeddings', help='Image embeedings file')
	parser.add_argument('--ignored', dest='ignored', help='Ignored examples', default=None)
	parser.add_argument('--meta', dest='meta', help='Metadata file')
	parser.add_argument('--y-meta', dest='y_meta', help='Metadata column name')
	parser.add_argument('--output-file', dest='output_file', help='Destination file')
	args = parser.parse_args()
	main(args.embeddings, args.meta, args.y_meta, args.output_file, args.ignored)