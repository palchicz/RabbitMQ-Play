#!/usr/bin/env python
from __future__ import print_function
import pika
import sys

connection_params = pika.ConnectionParameters(host='dockerhost')
connection = pika.BlockingConnection(connection_params)
channel = connection.channel()

channel.exchange_declare(
    exchange='topic_logs',
    type='topic'            # Must match routing key
)

queue = channel.queue_declare(exclusive=True)
queue_name = queue.method.queue

binding_keys = sys.argv[1:]
if not binding_keys:
    print(
        "Usage: {} [binding_key]...".format(sys.argv[0]),
        file=sys.stderr
    )
    sys.exit(1)

for binding_key in binding_keys:
    channel.queue_bind(
        exchange='topic_logs',
        queue=queue_name,       # Name of the queue to bind
        routing_key=binding_key # Must match routing key
    )

print(" [*] Waiting for logs. To exit press CTRL+C")

def callback(ch, method, properties, body):
    print(" [x] {}:{}".format(method.routing_key, body))

channel.basic_consume(callback, queue=queue_name, no_ack=True)
channel.start_consuming()
