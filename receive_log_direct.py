#!/usr/bin/env python
from __future__ import print_function
import pika
import sys

connection_param = pika.ConnectionParameters(host='dockerhost')
connection = pika.BlockingConnection(connection_param)
channel = connection.channel()

channel.exchange_declare(
    exchange='direct_logs',
    type='direct'           # Must give binding key to connect
)

queue = channel.queue_declare(exclusive=True)
queue_name = queue.method.queue

severities = sys.argv[1:]
if not severities:
    print(
        "Usage: {} [info] [warning] [error]".format(sys.argv[0]),
        file=sys.stderr
    )
    sys.exit(1)

for severity in severities:
    channel.queue_bind(
        exchange='direct_logs',     # Exchange name
        queue=queue_name,           # Queue name
        routing_key=severity        # Only receive msgs with routing_key == severity
    )

print(" [*] Waiting for logs. To exit press CTRL+C")

def callback(ch, method, properties, body):
    print(" [x] {}:{}".format(method.routing_key, body))

channel.basic_consume(callback, queue=queue_name, no_ack=True)
channel.start_consuming()
