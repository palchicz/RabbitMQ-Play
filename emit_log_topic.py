#!/usr/bin/env python
import pika
import sys

connection_params = pika.ConnectionParameters(host='dockerhost')
connection = pika.BlockingConnection(connection_params)
channel =  connection.channel()

channel.exchange_declare(
    exchange='topic_logs',
    type='topic'
)

routing_key = sys.argv[1] if len(sys.argv) > 1 else 'anonymous.info'
message = " ".join(sys.argv[2:]) or 'Hello World!'
channel.basic_publish(
    exchange='topic_logs',
    routing_key=routing_key, # Only send msg to queues that match `routing_key`
    body=message
)

print(" [x] Sent {}:{}".format(routing_key, message))
connection.close()
