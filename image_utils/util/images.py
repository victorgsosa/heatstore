import base64
import cv2
import io
import numpy as np


def image_size(image):
	image_np = np.fromstring(image, np.uint8)
	image_decoded = cv2.imdecode(image_np, cv2.IMREAD_COLOR)
	return image_decoded.shape[1], image_decoded.shape[0]

def read_base64(str_base64):
	sbuf = io.BytesIO()
	sbuf.write(base64.b64decode(str_base64))
	return sbuf.getvalue()