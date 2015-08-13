#!/usr/bin/env python
import pika
import sys

connection_params = pika.ConnectionParameters(host='dockerhost')
connection = pika.BlockingConnection(connection_params)
channel = connection.channel()

channel.exchange_declare(
    exchange='direct_logs',
    type='direct'           # Only send msgs matching routing_key
)

severity = sys.argv[1] if len(sys.argv) > 1 else 'info'
message = " ".join(sys.argv[2:]) or "Hello World!"
channel.basic_publish(
    exchange='direct_logs',
    routing_key=severity,   # Only send  msg to queues bound with `severity`
    body=message
)

print(" [x] Sent {}:{}".format(severity, message))
connection.close()
