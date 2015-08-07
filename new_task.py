import sys

import pika

# Create a connection to the rabbit service
connection = pika.BlockingConnection(pika.ConnectionParameters(
    'dockerhost'))
channel = connection.channel()

# Create the recipient queue
channel.queue_declare(queue='hello')

message = ' '.join(sys.argv[1:]) or "Hello World!"

# Send the message to the queue
channel.basic_publish(
    exchange='', routing_key='hello', body=message)

print(" [x] Sent {}".format(message))
connection.close()
