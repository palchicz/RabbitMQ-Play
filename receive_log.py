#!/usr/bin/env python
import pika

connection_param = pika.ConnectionParameters(host='dockerhost')
connection = pika.BlockingConnection(connection_param)
channel = connection.channel()

channel.exchange_declare(
    exchange='logs',    # Name the exchange where we send msgs
    type='fanout'       # The exchange will fwd msgs to all queues
)

# Create a queue with (a) a random name and (b) will terminate
# when the receiver terminates
queue = channel.queue_declare(exclusive=True)

# Get the random name of the queue
queue_name = queue.method.queue

# Bind the queue to the logs exchange
channel.queue_bind(exchange='logs', queue=queue_name)

print(" [*] Waiting for logs. To exit press CTRL+C")

def callback(ch, method, properties, body):
    print(" [x] {}".format(body))

channel.basic_consume(callback, queue=queue_name, no_ack=True)
channel.start_consuming()
