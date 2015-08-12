#!/usr/bin/env python
import pika
import sys

connection_params = pika.ConnectionParameters(host='dockerhost')
connection = pika.BlockingConnection(connection_params)
channel = connection.channel()

# Create the exchange for msgs
channel.exchange_declare(
    exchange='logs',    # Name the exchange where we send msgs
    type='fanout'       # The exchange will fwd msgs to all queues
)

message = ' '.join(sys.argv[1:]) or "info: Hellow World!"
channel.basic_publish(
    exchange='logs',    # Exchange to publish to, '' is default
    routing_key='',     # Queue to fwrd msg to, '' is any queue
    body=message
)

print(" [x] Sent {}".format(message))
connection.close()

