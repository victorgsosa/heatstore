import base64
import cv2
import io
import numpy as np

from PIL import Image


def image_size(image):
	image_decoded = byte_string_to_cv(image)
	return image_decoded.shape[1], image_decoded.shape[0]

def read_base64(str_base64):
	sbuf = io.BytesIO()
	sbuf.write(base64.b64decode(str_base64))
	return sbuf.getvalue()

def to_base64(byte_image):
	return base64.b64encode(byte_image).decode('utf-8')

def cv_to_byte_string(cv_image):
	pil_image = Image.fromarray(cv_image)
	output_io = io.BytesIO()
	pil_image.save(output_io, format='JPEG')
	return output_io.getvalue()

def cv_to_base64(cv_image):
	byte_image = cv_to_byte_string(cv_image)
	return to_base64(byte_image)

def byte_string_to_cv(byte_image):
	image_np = np.fromstring(byte_image, dtype=np.uint8)
	return cv2.imdecode(image_np, cv2.IMREAD_COLOR)

def base64_to_cv(base64_image):
	byte_image = read_base64(base64_image) 
	return byte_string_to_cv(byte_image)

def byte_string_to_cv_rgb(byte_image):
	cv_image =  byte_string_to_cv(byte_image)
	return cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)