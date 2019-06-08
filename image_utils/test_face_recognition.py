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
from services.face_detector.classifiers import SVMFaceClassifier, NNFaceClassifier


logger = logging.getLogger(__name__)



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
	embeddings = Facenet(FacenetModel('resources/face_detection/frozen_facenet.pb'))

	age_classifier = NNFaceClassifier()
	age_classifier.load('age.meta')
	first_image = None
	while(True):
		ret, image = cap.read()
		aligned_image = _align_image(image, aligner, default_image_size)

		if aligned_image is not None:
			pil_image = Image.fromarray(aligned_image)
			output_io = io.BytesIO()
			pil_image.save(output_io, format='JPEG')
			face_embeddings = embeddings.detect([output_io.getvalue()])[0]
			age = age_classifier.predict(np.expand_dims(face_embeddings, 0))[0]
			if first_image is None:
				first_image = face_embeddings
			distance = np.linalg.norm(first_image-face_embeddings)
			print("Distance: %.3f Victor: %s Age Range %s" % (distance, distance < 1.1,  age))
			cv2.imshow('aligned', aligned_image)
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break
	# When everything done, release the capture
	cap.release()
	cv2.destroyAllWindows()

