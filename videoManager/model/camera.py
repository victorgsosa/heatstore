
class Camera:
	pass

	def __init__(self,cData):
		pass
		self._id=cData['id']
		self._name=cData['name']
		self._url=cData['url']
		self._msgtp=cData['msgType']
		self._token=cData['token']
		self._capfreq=cData['cap_freq']
		self._dim=cData['dim']
		self._k=cData['k']
		self._d=cData['d']