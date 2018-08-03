import numpy as np
import cv2
import io
import datetime
import argparse
import tensorflow as tf
import os
import logging
import scipy.io
import sys

from PIL import Image
from services.face_detector.align_dlib import AlignDlib
from services.face_detector.facenet import Facenet, FacenetModel, default_image_size

aligner =  AlignDlib('resources/face_detection/shape_predictor_68_face_landmarks.dat')
embeddings = Facenet(FacenetModel('resources/face_detection/frozen_facenet.pb'))

def _align_image(image, crop_size):
	bb = aligner.getLargestFaceBoundingBox(image)
	aligned = aligner.align(crop_size, image, bb, landmarkIndices=AlignDlib.INNER_EYES_AND_BOTTOM_LIP)
	if aligned is not None:
		aligned = cv2.cvtColor(aligned, cv2.COLOR_BGR2RGB)
	return aligned

def _image_embeddings(image):
	pil_image = Image.fromarray(image)
	output_io = io.BytesIO()
	pil_image.save(output_io, format='JPEG')
	face_embeddings = embeddings.detect([output_io.getvalue()])
	return face_embeddings[0]

def matlab2datetime(matlab_datenum):
    day = datetime.datetime.fromordinal(int(matlab_datenum))
    dayfrac = datetime.timedelta(days=matlab_datenum%1) - datetime.timedelta(days = 366)
    return day + dayfrac


def process_image(image, crop_size):
	aligned_image = _align_image(image, crop_size)
	if aligned_image is None:
		return None
	else:
		return _image_embeddings(aligned_image)


def process_dataset(name, data_dir, image_files, output_dir, meta, crop_size=default_image_size, batch_size=1000):
	assert name in ['train', 'test', 'val']
	i = 0
	filename = os.path.join(output_dir, 'embeddings.tar.gz')
	try:
		os.remove(filename)
	except OSError:
		pass
	print("Processing %s dataset with %i images" % (name, len(image_files)))
	ignored_images = []
	image_embeddings = []
	with open(filename,'ab') as f:
		for image_file in image_files:
			i = i + 1
			image = cv2.imread(os.path.join(data_dir, image_file))
			rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
			embeddings  = process_image(rgb_image, crop_size)
			if embeddings is None:
				print("Image %s does not contains a face, ignored" % image_file)
				ignored_images.append(i)
			else:
				image_embeddings.append(embeddings)
			if i % batch_size == 0:
				print("%i images processed" % i)
				np.savetxt(f, np.array(image_embeddings), delimiter=",")
				f.flush()
				os.fsync(f.fileno())
				image_embeddings = []
	print("%s dataset processed" % name)
	return ignored_images



def main(meta_filename, data_dir, output_dir, crop_size=default_image_size, batch_size=1000):
	meta = scipy.io.loadmat(meta_filename, squeeze_me=True)['imdb']
	ignored_images = process_dataset('train', data_dir, meta['full_path'].tolist(), output_dir, meta, crop_size, batch_size)
	print("ignored images: %s" % ignored_images)
	ignored_filename = os.path.join(output_dir, 'ignored_images.txt')
	try:
		os.remove(ignored_filename)
	except OSError:
		pass
	with open(ignored_filename,'w') as f:
		np.savetxt(f, np.array(ignored_images, dtype=np.int64), delimiter=",")

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('--data-dir', dest='data_dir', help='Trainig data dir')
	parser.add_argument('--meta', dest='meta', help='Metadata file')
	parser.add_argument('--output-dir', dest='output_dir', help='Output data dir')
	parser.add_argument('--crop-size', dest='crop_size', help='Crop size', default=default_image_size)
	parser.add_argument('--batch-size', dest='batch_size', help='Batch size', default=1000)
	args = parser.parse_args()
	main(args.meta, args.data_dir, args.output_dir, args.crop_size)