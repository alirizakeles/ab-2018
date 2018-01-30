#!/usr/bin/env python
import pika
from json import dumps
QUEUE_NAME = 'gitlab-worker-queue'
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
USER_NAMES = ['lbennett', 'tauriedavis']

channel.queue_declare(queue=QUEUE_NAME)

channel.basic_publish(exchange='',
                      routing_key=QUEUE_NAME,
                      body=dumps(USER_NAMES))
print(" [x] Sent 'Hello World!'")
connection.close()