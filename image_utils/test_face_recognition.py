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
from services.face_detector.classifiers.svm_face_classifier import SVMFaceClassifier


logger = logging.getLogger(__name__)



def _align_image(image, aligner, crop_dim):
	bb = aligner.getLargestFaceBoundingBox(image)
	aligned = aligner.align(crop_dim, image, bb, landmarkIndices=AlignDlib.INNER_EYES_AND_BOTTOM_LIP)
	if aligned is not None:
		aligned = cv2.cvtColor(aligned, cv2.COLOR_BGR2RGB)
	return aligned



if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('-s', '--source', dest='source',type=int, default=0, help='Device index')
	args = parser.parse_args()
	cap = cv2.VideoCapture(args.source)
	aligner =  AlignDlib('resources/face_detection/shape_predictor_68_face_landmarks.dat')
	embeddings = Facenet(FacenetModel('resources/face_detection/frozen_facenet.pb'))
	gender_classifier = SVMFaceClassifier()
	gender_classifier.load('resources/face_detection/gender.pkl')
	first_image = None
	while(True):
		ret, image = cap.read()
		rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
		aligned_image = _align_image(image, aligner, default_image_size)

		if aligned_image is not None:
			pil_image = Image.fromarray(aligned_image)
			output_io = io.BytesIO()
			pil_image.save(output_io, format='JPEG')
			face_embeddings = embeddings.detect([output_io.getvalue()])[0]
			gender = gender_classifier.predict(np.expand_dims(face_embeddings, 0))[0]
			gender_p = gender_classifier.predict_proba(np.expand_dims(face_embeddings, 0))[0]
			if first_image is None:
				first_image = face_embeddings
			distance = np.linalg.norm(first_image-face_embeddings)
			print("Distance: %.3f Victor: %s Gender %s - %s%" % (distance, distance < 1.1, "Male" if gender == 1.0 else "Female", gender_p * 100))
			show_image = cv2.cvtColor(aligned_image, cv2.COLOR_RGB2BGR)
			cv2.imshow('aligned', show_image)
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break
	# When everything done, release the capture
	cap.release()
	cv2.destroyAllWindows()

