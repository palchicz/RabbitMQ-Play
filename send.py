#!/usr/bin/env python
import pika

# Create a connection to the rabbit service
connection = pika.BlockingConnection(pika.ConnectionParameters(
    'dockerhost'))
channel = connection.channel()

# Create the recipient queue
channel.queue_declare(queue='hello')

# Send the message to the queue
channel.basic_publish(
    exchange='', routing_key='hello', body='Hello World!')

print(" [x] Sent 'Hello World'")

# Close the connection
connection.close()
