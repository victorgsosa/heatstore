import argparse
import datetime as dt
import numpy as np
import scipy.io
import random

from services.face_detector.classifiers import SVMFaceClassifier
from services.face_detector.classifiers import NNFaceClassifier




def svm():
	return SVMFaceClassifier()

def nn():
	return NNFaceClassifier()

model_types = {
	'SVM': svm,
	'NN': nn
}

def train(model_type, embeddings, classes, output_file):
	classifier = model_types[model_type]()
	classifier.train(embeddings, classes)
	classifier.save(output_file)

def sample(embeddings, classes, size):
	indexes = np.random.randint(0, embeddings.shape[0], size)
	return embeddings[indexes], classes[indexes]


def matlab2datetime(matlab_datenum):
	day = dt.datetime.fromordinal(int(matlab_datenum))
	dayfrac = dt.timedelta(days=int(matlab_datenum)%1) - dt.timedelta(days = 366)
	try:
		return (day + dayfrac)
	except OverflowError:
		pass

def calculate_age(meta):
	dob = np.array([matlab2datetime(d) for d in meta['dob'].tolist()], dtype='datetime64')
	print(dob)
	photo_taken = np.array([ dt.datetime(year=y, month=7, day=1) for y in meta['photo_taken'].tolist()], dtype='datetime64')
	print(photo_taken)
	ages = ((photo_taken - dob) / 3650).astype(np.uint8) 
	ages[ages>10] = 10
	return ages 


def main(model_type, embeddings_file, meta_filename, y_meta, output_file, ignored_examples_file=None, face_score_threshold=3):
	meta = scipy.io.loadmat(meta_filename, squeeze_me=True)['imdb']
	print('Metadata readed')
	if y_meta == 'age':
		y = calculate_age(meta)
		print(y)
	else:
		y = np.array(meta[y_meta].tolist(), dtype=np.uint8)

	length = embeddings.shape[0]
	score = np.array(meta["face_score"].tolist(), dtype=np.float32)
	if ignored_examples_file:
		print('Removing ignored images...')
		with open(ignored_examples_file, 'rb') as f:
			ignored_examples = np.loadtxt(ignored_examples_file, delimiter=',').astype(np.int64)
		length = length + ignored_examples.shape[0]
		y = y[0:length]
		used = np.ones(y.shape[0], dtype=np.int64)
		used[ignored_examples] = 0
		y = np.compress(used, y)
		score = np.compress(used, score)
	else:
		y = y[0:length]
		score = score[0:length]
	np.random.seed(0)
	embeddings = embeddings[~np.isnan(y)]
	score = score[~np.isnan(y)]
	y = y[~np.isnan(y)]

	embeddings = embeddings[score>face_score_threshold]
	y = y[score>face_score_threshold]

	#sample = np.random.randint(0, embeddings.shape[0], 5000)
	#embeddings, y = (embeddings[sample], y[sample])
	#print(y)
	print('Training with %d images' % embeddings.shape[0])
	train(model_type, embeddings, y, output_file)


if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('--embeddings', dest='embeddings', help='Image embeedings file')
	parser.add_argument('--ignored', dest='ignored', help='Ignored examples', default=None)
	parser.add_argument('--meta', dest='meta', help='Metadata file')
	parser.add_argument('--y-meta', dest='y_meta', help='Metadata column name')
	parser.add_argument('--output-file', dest='output_file', help='Destination file')
	parser.add_argument('--type', dest='model_type', help='Model type (SVM, NN)')
	args = parser.parse_args()
	main(args.model_type, args.embeddings, args.meta, args.y_meta, args.output_file, args.ignored)