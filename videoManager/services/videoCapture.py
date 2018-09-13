from model.camera import Camera
from services.iotStream import sendIot
from datetime import datetime
import _thread
import cv2
import os
import base64
import math
import threading
import time
import numpy as np

class VideoCapture:
	pass

	#DIM=(1280, 720)
	#K=np.array([[891.7489340683804, 0.0, 676.2188454314042], [0.0, 897.2239855804237, 405.7293137278092], [0.0, 0.0, 1.0]])
	#D=np.array([[-0.20806507742892744], [0.12946991645680045], [-0.18885159067031906], [0.09064495701857257]])



	def __init__(self, Camera):
		pass

		self._pid = os.getpid()
		self._camera=Camera
		self._inittime=int(datetime.now().timestamp())
		self.photo=False
		self.K=np.array(Camera._k)
		self.D=np.array(Camera._d)
		if len(self.K)>0:
			pass
			self.DIM=(Camera._dim[0],Camera._dim[1])
		else:
			self.DIM=()
		self.play()

	def sendMsg(self,imagebin):
		pass
		message = [{
					"timestamp": int(datetime.now().timestamp()),
					"imagetype": 'image/png',
					"imagecod": 'base64',
					"image": str(imagebin)[2:-1]
				}]
		print("Enviando imagen camara",self._camera._name)
		sendIot(self._camera._id,self._camera._token,self._camera._msgtp,message)

	def shooting(self):
		pass
		self.photo=True
		print("Rise timer seconds: ",self._camera._capfreq)

	def undistort(self, img):
		h,w = img.shape[:2]
		map1, map2 = cv2.fisheye.initUndistortRectifyMap(self.K, self.D, np.eye(3), self.K, self.DIM, cv2.CV_16SC2)
		undistorted_img = cv2.remap(img, map1, map2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)
		return undistorted_img

	def play(self):
		pass
		ret=True
		frame=[]
		print (self._pid)
		cap = cv2.VideoCapture(self._camera._url)
		timer=threading.Timer(self._camera._capfreq,self.shooting)
		timer.start()
		print("TIMER",timer)
		img_counter = 0
		while(True):
		    # Capture frame-by-frame
			ret, frame = cap.read()
			#gray=cv2.resize(frame,(800,600))
		    # Display the resulting frame
			if ret:
				pass
				if len(self.K)>0:
					pass
					frame = self.undistort(frame)
				cv2.imshow('frame',frame)

				if (self.photo):
					pass
					self.photo = False
					timer=threading.Timer(self._camera._capfreq,self.shooting)
					timer.start()
					ret, img_buf=cv2.imencode('.png',frame)
					imagebin=base64.b64encode(img_buf)
					try:
						_thread.start_new_thread(self.sendMsg,(imagebin,))
					except:
						print ("Error: unable to start thread")
						timer.cancel()

				k = cv2.waitKey(1)
				if k%256 == 27:
			        # ESC pressed
					print("Escape hit, closing..."+str(self._camera._url))
					timer.cancel()
					break
				elif k%256 == 32:
			        # SPACE pressed take and save picture
					self.photo=True
					#img_name = "calibrator/summit_frame_{}.png".format(img_counter)
					#cv2.imwrite(img_name, frame)
					#print("{} written!".format(img_name))
					#img_counter += 1


		# When everything done, release the capture
		cap.release()
		cv2.destroyAllWindows()
		