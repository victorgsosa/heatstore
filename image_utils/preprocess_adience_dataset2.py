import numpy as np
import cv2
import io
import datetime
import argparse
import os
import datetime as dt
import pandas as pd
import sys
import shutil

from PIL import Image
from services.face_detector.align_dlib import AlignDlib
from services.face_detector.facenet import Facenet, FacenetModel, default_image_size

aligner =  AlignDlib('resources/face_detection/shape_predictor_68_face_landmarks.dat')
embeddings = Facenet(FacenetModel('resources/face_detection/frozen_facenet.pb'))

def _align_image(image, crop_size):
	bb = aligner.getLargestFaceBoundingBox(image)
	aligned = aligner.align(crop_size, image, bb, landmarkIndices=AlignDlib.INNER_EYES_AND_BOTTOM_LIP)
	return aligned

def _image_embeddings(image):	
	face_embeddings = embeddings.detect([output_io.getvalue()])
	return face_embeddings[0]

def matlab2datetime(matlab_datenum):
	day = dt.datetime.fromordinal(int(matlab_datenum))
	dayfrac = dt.timedelta(days=int(matlab_datenum)%1) - dt.timedelta(days = 366)
	try:
		return (day + dayfrac)
	except OverflowError:
		pass

def calculate_age(meta):
	dob = np.array([matlab2datetime(d) for d in meta['dob'].tolist()], dtype='datetime64')
	photo_taken = np.array([ dt.datetime(year=y, month=7, day=1) for y in meta['photo_taken'].tolist()], dtype='datetime64')
	ages = ((photo_taken - dob) / 3650).astype(np.uint8) 
	ages[ages>10] = 10
	return ages 


def process_image(image, crop_size):
	aligned_image = _align_image(image, crop_size)
	if aligned_image is None:
		return None
	else:
		return _image_embeddings(aligned_image)


def process_dataset(data_dir, image_files, output_dir, labels, crop_size=default_image_size):
	for image_file, label in zip(image_files, labels):
		image = cv2.imread(os.path.join(data_dir, image_file))
		if image is not None:
			rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
			aligned_image = _align_image(rgb_image, crop_size)
			if aligned_image is not None:
				label_dir = os.path.join(output_dir, str(label))
				if not os.path.exists(label_dir):
					os.makedirs(label_dir)
				print(os.path.join(label_dir, os.path.basename(image_file)))
				cv2.imwrite(os.path.join(output_dir, str(label), os.path.basename(image_file)), cv2.cvtColor(aligned_image, cv2.COLOR_RGB2BGR))
	print("dataset processed")



def main(meta_filename, data_dir, output_dir, y_meta, crop_size=default_image_size):
	print("Reading metadata...")
	meta = pd.read_csv(meta_filename, delimiter='\t')
	print("Metadata readed")
	if not os.path.exists(output_dir):
		os.makedirs(output_dir)
	meta['full_path'] = meta['user_id'] + '/coarse_tilt_aligned_face.' + meta['face_id'].astype(str) + '.' + meta['original_image']
	print(meta)
	process_dataset(data_dir, meta['full_path'], output_dir, meta[y_meta], crop_size)


if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('--data-dir', dest='data_dir', help='Trainig data dir')
	parser.add_argument('--meta', dest='meta', help='Metadata file')
	parser.add_argument('--output-dir', dest='output_dir', help='Output data dir')
	parser.add_argument('--y-meta', dest='y_meta', help='Metadata column name')
	parser.add_argument('--crop-size', dest='crop_size', help='Crop size', type=int, default=default_image_size)
	args = parser.parse_args()
	main(args.meta, args.data_dir, args.output_dir, args.y_meta, args.crop_size)