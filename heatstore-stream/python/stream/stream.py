import json
import threading

from .images import base64_to_cv
from .subscriber import Subscriber


LOCATION_EXCHANGE = 'LOCATOR'
CLASSIFICATION_EXCHANGE = 'CLASSIFICATOR'

class HeatstoreStream(object):
	def __init__(self, host, user, password, service, callback, port = 5672):
		url = 'amqp://%s:%s@%s:%s' % (user, password, host, port)
		self._subscriber = Subscriber(url, service, self._process_exchange)
		self._callback = callback
		t = threading.Thread(target=self._subscriber.run)
		t.daemon = True
		t.start()

	def _process_exchange(self, channel, method, properties, body):
		images = json.loads(body)
		for image in images:
			cv = base64_to_cv(image['content'])
			del image['content']
			self._callback(cv, image)



		