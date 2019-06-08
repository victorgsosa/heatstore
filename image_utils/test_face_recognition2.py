import numpy as np
import cv2
import io
import argparse
import tensorflow as tf
import os
import logging

from PIL import Image
from services.face_detector.align_dlib import AlignDlib
from services.face_detector.facenet import Facenet, FacenetModel, default_image_size
from services.face_detector.classifiers import SVMFaceClassifier, NNFaceClassifier, ResNetFaceClassifier


logger = logging.getLogger(__name__)
image_size = 160


def _align_image(image, aligner, crop_dim):
	bb = aligner.getLargestFaceBoundingBox(image)
	aligned = aligner.align(crop_dim, image, bb, landmarkIndices=AlignDlib.INNER_EYES_AND_BOTTOM_LIP)
	return aligned



if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('-s', '--source', dest='source',type=int, default=0, help='Device index')
	args = parser.parse_args()
	cap = cv2.VideoCapture(args.source)
	aligner =  AlignDlib('resources/face_detection/shape_predictor_68_face_landmarks.dat')

	age_classifier = ResNetFaceClassifier('age')
	age_classifier.load('resources/face_detection/age.h5')
	gender_classifier = ResNetFaceClassifier('gender')
	gender_classifier.load('resources/face_detection/gender.h5')
	first_image = None
	while(True):
		ret, image = cap.read()
		aligned_image = _align_image(image, aligner, default_image_size)

		if aligned_image is not None:
			resized_image = cv2.resize(aligned_image, (image_size, image_size))
			resized_image = resized_image / 1./255
			resized_image = np.expand_dims(resized_image, 0)
			age = age_classifier.predict(resized_image)[0]
			gender = gender_classifier.predict(resized_image)[0]
			age_proba = age_classifier.predict_proba(resized_image)[0]
			gender_proba = gender_classifier.predict_proba(resized_image)[0]
			print("Age Range %s prob %s Gender %s prob %s"  % (age, age_proba, gender, gender_proba))
			cv2.imshow('aligned', aligned_image)
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break
	# When everything done, release the capture
	cap.release()
	cv2.destroyAllWindows()

