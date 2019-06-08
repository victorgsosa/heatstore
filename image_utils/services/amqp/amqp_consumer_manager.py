import pika
import threading
import logging

from .consumer import Consumer
from .subscriber import Subscriber

log = logging.getLogger(__name__)

class AMQPConsumerManager(object):
	def __init__(self, amqp_url):
		self.amqp_url = amqp_url
		self.consumers = []
		self.subscribers = []

	def add_consumer(self, queue, callback, durable=False):
		log.info('Adding %s queue with callback %s', queue, callback)
		self.consumers.append(Consumer(self.amqp_url, queue, callback, durable))

	def subscribe(self, exchange, callback):
		log.info('Adding to exchange %s with callback %s', exchange, callback)
		self.subscribers.append(Subscriber(self.amqp_url, exchange, callback))

	def start(self):
		for consumer in self.consumers:
			t = threading.Thread(target=consumer.run)
			t.daemon = True
			t.start()
		for subscriber in self.subscribers:
			t = threading.Thread(target=subscriber.run)
			t.daemon = True
			t.start()
		


	def start_consumer(self, amqp_url, queue, callback, no_ack):
		connection = pika.BlockingConnection(pika.URLParameters(amqp_url))
		channel = connection.channel()
		channel.queue_declare(queue=queue, durable=True)
		channel.basic_consume(callback,
                      queue=queue,
                      no_ack=no_ack)
		channel.start_consuming()

	def start_subscriber(self, amqp_url, exchange, callback, no_ack):
		connection = pika.BlockingConnection(pika.URLParameters(amqp_url))
		channel = self.connection.channel()
		channel.exchange_declare(exchange=exchange,
                         exchange_type='fanout')
		result = channel.queue_declare(exclusive=True)
		channel.queue_bind(exchange=exchange,
                   queue=result.method.queue)
		channel.basic_consume(callback,
                      queue=result.method.queue,
                      no_ack=no_ack)
		channel.start_consuming()




