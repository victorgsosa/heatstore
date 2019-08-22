import cv2
import time

from stream import HeatstoreStream, CLASSIFICATION_EXCHANGE

AGE_CLASSES = {0: '(0, 2)', 1:'(15, 25)', 2:'(25, 35)' , 3:'(35, 43)', 4:'(2, 8)', 5:'(48, 53)', 6:'(60, 100)', 7:'(8, 15)'}
SENTIMENT_CLASSES = {0:'negative', 1:'neutral', 2:'positive'}
GENDER_CLASSES = {0: 'Female', 1: 'Male'}

class Streamer(object):
	def __init__(self):
		self._image = None
		self._data = None

	def process(self, image, data):
		self._image = image
		self._data = data

	def start(self):
		while(True):
			if  self._image is not None:
				image = self._image
				for i in range(len(self._data['detections'])):
					detection = self._data['detections'][i]
					classification = self._data['classes'][i]
					gender = GENDER_CLASSES[classification['gender']['value']] if 'gender' in classification else None
					age = AGE_CLASSES[classification['age']['value']] if 'age' in classification else None
					sentiment = SENTIMENT_CLASSES[classification['sentiment']['value']] if 'sentiment' in classification else None
					classes = "Gender: %s Age: %s Sentiment %s" % (gender, age, sentiment)
					xMin = int(detection['xMin'])
					yMin = int(detection['yMin'])
					xMax = int(detection['xMax'])
					yMax = int(detection['yMax'])
					image = cv2.rectangle(image, (xMin, yMin),(xMax, yMax),(0,255,255), 1)
					cv2.putText(image, classes, (xMin, yMin-5), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0,255,255), 1) 
				cv2.imshow('video', self._image)
			if cv2.waitKey(1) & 0xFF == ord('q'):
				break

if __name__ == '__main__':
	processor = Streamer()
	stream = HeatstoreStream('18.221.86.9', 'guest', 'guest', CLASSIFICATION_EXCHANGE, processor.process)
	processor.start()
	
