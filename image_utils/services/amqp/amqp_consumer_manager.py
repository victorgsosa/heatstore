import pika
import threading
import logging

log = logging.getLogger(__name__)

class AMQPConsumerManager(object):
	def __init__(self, amqp_url):
		self.amqp_url = amqp_url
		self.consumers = []
		self.subscribers = []

	def add_consumer(self, queue, callback, no_ack=True):
		connection = pika.BlockingConnection(pika.URLParameters(self.amqp_url))
		log.info('Listening %s queue on %s with callback %s', queue, connection, callback)
		channel = connection.channel()
		channel.queue_declare(queue=queue, durable=True)
		channel.basic_consume(callback,
                      queue=queue,
                      no_ack=no_ack)
		t = threading.Thread(target=channel.start_consuming)
		t.daemon = True
		t.start()
		self.consumers.append({
			'queue' : queue,
			'channel': channel,
			'thread': t
			})

	def subscribe(self, exchange, callback, no_ack=True):
		connection = pika.BlockingConnection(pika.URLParameters(self.amqp_url))
		log.info('Subscribing to exchange on %s with callback %s', exchange, connection, callback)
		channel = connection.channel()
		channel.exchange_declare(exchange=exchange,
                         exchange_type='fanout')
		result = channel.queue_declare(exclusive=True)
		channel.queue_bind(exchange=exchange,
                   queue=result.method.queue)
		channel.basic_consume(callback,
                      queue=result.method.queue,
                      no_ack=no_ack)
		t = threading.Thread(target=channel.start_consuming)
		t.daemon = True
		t.start()
		self.consumers.append({
			'exchange' : exchange,
			'channel': channel,
			'thread': t
			})



