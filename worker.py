#!/usr/bin/env python
import time

import pika

# Connect to RabbitMQ
connection_params = pika.ConnectionParameters('dockerhost')
connection = pika.BlockingConnection(connection_params)

channel = connection.channel()

# Make sure the queue exists
# Good practice to do this for both sender and receiver b/c
# not clear who is invoked first
channel.queue_declare(queue='hello')

# Declare a callback function to be executed when the message is
# received. This call back does a second of work for each `.`
# in a message
def callback(ch, method, properties, body):
    print(" [x] Received {}".format(body))
    time.sleep(body.count('.'))
    print(" [x] Done")


# Register the callback with Pika
channel.basic_consume(callback, queue='hello', no_ack=True)
print(' [*] Waiting for messages. To exit, press CTRL+C')
channel.start_consuming()
