import unittest
import numpy as np
from services.image_locator.locator import ImageLocatorCalibrator, ImageLocator

class TestImageLocatorCalibrator(unittest.TestCase):

	def test_calibrate(self):
		calibrator = ImageLocatorCalibrator(focal_length=0.02, measures={
			'distance': np.array([1, 1.5, 2]),
			'values': np.array([[100, 200], [300, 400], [400, 300]])
			})
		calibrator.calibrate()
		np.testing.assert_allclose(calibrator.x, np.array([-0.14235033, 0.690983004, 4982.261536]), rtol=1e-6)

class TestImageLocator(unittest.TestCase):

	def setUp(self):
		self.locator = ImageLocator(calibrator = ImageLocatorCalibrator(focal_length=0.02, measures={
			'distance': np.array([3, 2.5, 4]),
			'values': np.array([[100, 200], [300, 400], [400, 300]])
			}))


	def test_distance_with_calibration_points_must_be_the_same(self):
		distance = self.locator.distance(np.array([[100, 200], [300, 400], [400, 300]]))
		np.testing.assert_allclose(distance, np.array([3, 2.5, 4]))

	def test_locator(self):
		location = self.locator.locate(np.array([[100, 200], [300, 400], [400, 300]]), 2)
		np.testing.assert_allclose(location, np.array([[2.236067933, 0.000447214], [1.5, 0.0001], [3.464101611, 0.000173205]]), rtol=1e-4)
		print(location)

if __name__ == '__main__':
    unittest.main()