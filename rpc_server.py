#!/usr/bin/env python
import pika


connection_params = pika.ConnectionParameters(host='dockerhost')
connection = pika.BlockingConnection(connection_params)
channel = connection.channel()

# Queue name is rpc_queue, no exchange
channel.queue_declare(queue='rpc_queue')

def fib(n):
    if n == 0:
        return 0
    if n == 1:
        return 1
    else:
        return fib(n - 1) + fib(n - 2)

def on_request(ch, method, props, body):
    n = int(body)
    print(" [.] fib({})".format(n))
    response = fib(n)

    # Queue to publish to is stored in props
    # Correlation id is also stored in props
    ch.basic_publish(
        exchange='',
        routing_key=props.reply_to,
        properties=pika.BasicProperties(correlation_id = props.correlation_id),
        body=str(response)
    )

    # Acknowledge that the request has been responded to
    ch.basic_ack(delivery_tag=method.delivery_tag)

# Only buffer 1 request at a time
channel.basic_qos(prefetch_count=1)
channel.basic_consume(on_request, queue='rpc_queue')

print(" [x] Awaiting RPC requests")
channel.start_consuming()
