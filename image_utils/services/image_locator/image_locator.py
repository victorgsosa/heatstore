import numpy as np

from model.camera import Camera

class ImageLocatorCalibrator(object):

	def __init__(self, camera: Camera , measures):
		self.camera = camera
		self.measures = measures
		self.calibrated = False

	def calibrate(self):
		coef = np.hstack([self.measures['values'] , np.ones((3,1)) * self.camera.focal_length] )
		a = coef
		b = np.sqrt(np.sum(np.square(coef), axis=1)) / self.measures['distances']
		self.x = np.linalg.solve(a, b)
		self.calibrated = True


class ImageLocator(object):

	def __init__(self, calibrator: ImageLocatorCalibrator):
		if not calibrator.calibrated:
			calibrator.calibrate()
		self.calibrator = calibrator


	def distance(self, points):
		coef = np.hstack([points , np.ones((points.shape[0],1)) * self.calibrator.camera.focal_length])
		distance = np.sqrt(np.sum(np.square(coef), axis=1)) / np.sum(coef * self.calibrator.x, axis=1)
		return distance

	def locate(self, points):
		distance = self.distance(points)
		hdistance = np.sqrt(np.square(distance) - self.calibrator.camera.height * self.calibrator.camera.height )
		x = hdistance * np.sin(np.arctan(points[:,0] / self.calibrator.camera.focal_length))
		y = hdistance * np.cos(np.arctan(points[:,0] / self.calibrator.camera.focal_length))
		return np.column_stack((x,y))

