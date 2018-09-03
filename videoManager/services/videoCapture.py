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

class VideoCapture:
	pass

	def __init__(self, Camera):
		pass

		self._pid = os.getpid()
		self._camera=Camera
		self._inittime=int(datetime.now().timestamp())
		self.photo=False
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


	def play(self):
		pass
		ret=True
		frame=[]
		print (self._pid)
		cap = cv2.VideoCapture(self._camera._url)
		timer=threading.Timer(self._camera._capfreq,self.shooting)
		timer.start()
		print("TIMER",timer)
		while(True):
		    # Capture frame-by-frame
			ret, frame = cap.read()
			#gray=cv2.resize(frame,(800,600))
		    # Display the resulting frame
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
		        # SPACE pressed
				ret, img_buf=cv2.imencode('.png',frame)
				imagebin=base64.b64encode(img_buf)
				
				try:
					_thread.start_new_thread(self.sendMsg,(imagebin,))
				except:
					print ("Error: unable to start thread")


		# When everything done, release the capture
		cap.release()
		cv2.destroyAllWindows()
		