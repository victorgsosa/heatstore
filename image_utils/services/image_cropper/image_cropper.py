import cv2 
import util.images as im
import numpy as np

class ImageCropper(object):

	def crop(self, image, detections):
		cropped_images = []
		image_cv = im.byte_string_to_cv(image)
		for detection in detections:
			cropped_image = image_cv[
				int(detection["yMin"] ) : int(detection["yMax"] ), 
				int(detection["xMin"]) : int(detection["xMax"]) ]
			cropped_images.append(im.cv_to_byte_string(cv2.cvtColor(cropped_image, cv2.COLOR_BGR2RGB)))
		return cropped_images
