import requests
import json
import numpy as np

from model import Camera, Role, Action

class CameraService(object):

	def __init__(self, url):
		self.url = url

	def find_one(self, id):
		response = requests.get("%s/%s" % (self.url, id))
		if(response.ok):
			data = response.json()
			if data is not None:
				return Camera(
					float(data["focalLength"]),
					float(data["height"]),
					np.array([data["aDistance"], data["bDistance"], data["cDistance"]], dtype=np.float64),
					np.array([
						[data["aX"], data["aY"]],
						[data["bX"], data["bY"]],
						[data["cX"], data["cY"]],
					], dtype=np.float64),
					[ Role(role["id"], role["description"], 
						[Action(action["id"], action["description"]) for action in role["actions"]]) for role in data["roles"]])

