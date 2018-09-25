from services.videoCapture import VideoCapture
from model.camera import Camera
import multiprocessing as mp
import os
import json


def videoStreaming(camera):
	pass
	print("Lanzando camara",mp.current_process().name)
	vc = VideoCapture(camera)

cams=[0,'rtsp://admin:YWRZZS@192.168.1.35:554/11']

if __name__ == '__main__':
	#Cargar archivo de configuración
	cams=[]
	with open('./resources/camConfig.json') as f:
		camConfig = json.load(f)

	for d in camConfig:
		pass
		cams.append(Camera(d))

	#Multiprocesamiento por camara
	mp.set_start_method('spawn')
	procs=[]
	for x in cams:
		pass
		p = mp.Process(name=x._name,target=videoStreaming, args=(x,))
		p.start()		
		procs.append(p)
	
	for y in procs:
		pass
		y.join()

	while True:
		pass
		for y in procs:
			pass
			if not y.is_alive():
				pass
				for x in cams:
					pass
					print("X_NAME:",x._name)
					print("P_NAME:",p.name)
					print("Array legth",len(procs))
					if x._name == p.name:
						pass
						p = mp.Process(name=x._name,target=videoStreaming, args=(x,))
						p.start()
						procs.remove(y)		
						procs.append(p)
						p.join()
						break

	
	