import numpy as np
import logging

from model import Camera

log = logging.getLogger(__name__)

class ImageLocatorCalibrator(object):

	def __init__(self, camera: Camera ):
		self.camera = camera
		coef = np.hstack([self.camera.measures , np.ones((3,1)) * self.camera.focal_length ] )
		a = coef
		b = np.sqrt(np.sum(np.square(coef), axis=1)) / self.camera.distances
		self.x = np.linalg.solve(a, b)
		log.info("x %s" % self.x )
		self.calibrated = True


class ImageLocator(object):

	def _distance(self, calibrator, points):
		coef = np.hstack([points , np.ones((points.shape[0],1)) * calibrator.camera.focal_length])
		log.info("coef %s" % coef)
		distance = np.sqrt(np.sum(np.square(coef), axis=1)) / np.sum(coef * calibrator.x, axis=1)
		return distance

	def locate(self, camera, points):
		assert camera is not None
		calibrator = ImageLocatorCalibrator(camera)
		distance = self._distance(calibrator, points)
		log.info("distance %s" % distance)
		log.info("height %s" % calibrator.camera.height)
		hdistance = np.sqrt(np.square(distance) - calibrator.camera.height * calibrator.camera.height )
		x = hdistance * np.sin(np.arctan(points[:,0] / calibrator.camera.focal_length))
		y = hdistance * np.cos(np.arctan(points[:,0] / calibrator.camera.focal_length))
		return np.column_stack((x,y))

