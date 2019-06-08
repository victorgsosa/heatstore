import pika
import logging

LOGGER = logging.getLogger(__name__)

class BlockingPublisher(object):

	def __init__(self, amqp_url):
		self._url = amqp_url
		LOGGER.info("Openning a new connection on %s" % amqp_url)
		self._connection = pika.BlockingConnection(pika.URLParameters(amqp_url))
		self._channel = self._connection.channel()


	def get_channel(self):
		try:
			if self._channel.is_closed:
				self._channel = self._connection.channel()
		except pika.exceptions.ConnectionClosed:
			LOGGER.info("Reopenning connection")
			self._connection = pika.BlockingConnection(pika.URLParameters(self._url))
			self._channel = self._connection.channel()
		return self._channel


	def send_to_queue(self, queue, body, properties, routing_key=''):
		channel = self.get_channel()
		channel.queue_declare(queue=queue)
		channel.basic_publish(exchange='',
						routing_key=routing_key,
		                body=body,
		                properties=properties)

	def send_to_exchange(self, exchange, body, properties, exchange_type='fanout', routing_key = ''):
		channel = self.get_channel()
		channel.exchange_declare(exchange=exchange,
					exchange_type=exchange_type)
		channel.basic_publish(exchange=exchange,
								routing_key=routing_key,
			                    body=body,
			                    properties=properties)