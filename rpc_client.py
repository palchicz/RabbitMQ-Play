#!/usr/bin/env python
import pika
import uuid

class FibonacciRocClient(object):

    def __init__(self):
        connection_params = pika.ConnectionParameters(host='dockerhost')
        self.connection = pika.BlockingConnection(connection_params)
        self.channel = self.connection.channel()

        #Each client gets its own callback queue
        result = self.channel.queue_declare(exclusive=True)
        self.callback_queue = result.method.queue

        # When the client receives a response, it invokes `on_response`
        # It doesn't need to notify the server that it finished
        # and it consumes off the callback queue for this client
        self.channel.basic_consume(
            self.on_response,
            no_ack=True,
            queue=self.callback_queue
        )

        # Dynamic state to keep track of the reponse and corr_id
        self.response = None
        self.corr_id = None

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, n):
        self.response = None
        self.corr_id = str(uuid.uuid4())

        self.channel.basic_publish(
            exchange='',
            routing_key='rpc_queue',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id
            ),
            body=str(n)
        )

        # Block until the reponse is received. process_data_events prompts the connection to refresh
        while not self.response:
            self.connection.process_data_events()
        return int(self.response)

fibonacci_rpc = FibonacciRocClient()

print(" [x] Requesting fib(30)")
reponse = fibonacci_rpc.call(30)
print(" [.] Got {}".format(reponse))
