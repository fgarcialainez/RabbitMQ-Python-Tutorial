#!/usr/bin/env python

"""
In this part of the tutorial we'll deliver a message to multiple
consumers. This pattern is known as "publish/subscribe".

    https://www.rabbitmq.com/tutorials/tutorial-three-python.html
"""

import sys
import pika


def main():
    # Open a connection with RabbitMQ server
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    # Create a 'logs' exchange of type 'fanout'
    channel.exchange_declare(exchange='logs', exchange_type='fanout')

    # Create the message to publish
    message = ' '.join(sys.argv[1:]) or "info: Hello World!"

    # Publish the message to the logs exchange
    channel.basic_publish(exchange='logs', routing_key='', body=str.encode(message))
    print(" [x] Sent %r" % message)

    # Close the connection
    connection.close()


# Main script
if __name__ == '__main__':
    main()
