import unittest
import numpy as np
from services.image_locator.image_locator import ImageLocatorCalibrator, ImageLocator
from model import Camera

class TestImageLocatorCalibrator(unittest.TestCase):

	def test_calibrate(self):
		calibrator = ImageLocatorCalibrator( camera=Camera(0.02,4.2,
			distances=np.array([1, 1.5, 2]),
			measures=np.array([[100, 200], [300, 400], [400, 300]])
		))
		np.testing.assert_allclose(calibrator.x, np.array([-0.14235033, 0.690983004, 4982.261536]), rtol=1e-6)


if __name__ == '__main__':
    unittest.main()