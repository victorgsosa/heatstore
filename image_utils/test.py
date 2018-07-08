import numpy as np
import cv2
import io
import argparse

from PIL import Image
from services.image_detector.person_detector import PersonDetector, PersonDetectorModel


if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('-s', '--source', dest='source',type=int, default=0, help='Device index')
	parser.add_argument('-t', '--threshold', dest='threshold', type=float, default=0.9, help='Score threshold')
	args = parser.parse_args()
	cap = cv2.VideoCapture(args.source)
	detector = PersonDetector(PersonDetectorModel(path='resources/image_detector/frozen_inference_graph.pb'))

	while(True):
		ret, image = cap.read()
		rows = image.shape[0]
		cols = image.shape[1]
		print("rows %i cols %i" % (rows, cols))
		rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
		pil_image = Image.fromarray(rgb_image)
		output_io = io.BytesIO()
		pil_image.save(output_io, format='JPEG')
		detections = detector.detect([output_io.getvalue()])
		filetered_detetions = [ detection for detection in detections[0] if detection['score'] > args.threshold ]
		print(filetered_detetions)
		for detection in filetered_detetions:
	   		left = int(detection['xMin'] * cols)
	   		top = int(detection['yMin'] * rows)
	   		right = int(detection['xMax'] * cols)
	   		bottom = int(detection['yMax'] * rows)
	   		cv2.rectangle(image, (left, top), (right, bottom), color=(23, 230, 210), thickness=2 )
		cv2.imshow('detector', image)
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break

	# When everything done, release the capture
	cap.release()
	cv2.destroyAllWindows()