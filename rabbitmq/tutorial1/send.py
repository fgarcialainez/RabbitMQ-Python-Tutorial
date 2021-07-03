#!/usr/bin/env python

"""
In this part of the tutorial we'll write two small programs in Python; a producer (sender) that sends a single
message, and a consumer (receiver) that receives messages and prints them out. It's a "Hello World" of messaging.

    https://www.rabbitmq.com/tutorials/tutorial-one-python.html
"""

import pika


def main():
    # Open a connection with RabbitMQ server
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    # Create a 'hello' queue to which the message will be delivered
    channel.queue_declare(queue='hello')

    # Publish a message using the default exchange
    channel.basic_publish(exchange='', routing_key='hello', body=b'Hello World!')
    print(" [x] Sent 'Hello World!'")

    # Close the connection
    connection.close()


# Main script
if __name__ == '__main__':
    main()
