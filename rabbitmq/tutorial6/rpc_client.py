#!/usr/bin/env python

"""
In this tutorial we're going to use RabbitMQ to build an RPC system: a client and a scalable RPC server.

    https://www.rabbitmq.com/tutorials/tutorial-six-python.html
"""

import uuid
import pika


class FibonacciRpcClient(object):
    def __init__(self):
        # Initialize member variables
        self.corr_id = None
        self.response = None

        # Open a connection with RabbitMQ server
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()

        # Create the queue to get RPC responses
        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True)

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, n):
        self.response = None
        self.corr_id = str(uuid.uuid4())

        # Publish the message in the queue
        self.channel.basic_publish(
            exchange='',
            routing_key='rpc_queue',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=str.encode(str(n))
        )

        # Wait until we get the RPC response
        while self.response is None:
            self.connection.process_data_events()

        return int(self.response) if self.response else -1


def main():
    # Create the fibonacci client
    fibonacci_rpc = FibonacciRpcClient()

    # Log request
    print(" [x] Requesting fib(30)")

    # Perform the RPC call
    response = fibonacci_rpc.call(30)

    # Log response
    print(" [.] Got %r" % response)


# Main script
if __name__ == '__main__':
    main()
