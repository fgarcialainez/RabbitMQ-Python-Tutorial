#!/usr/bin/env python

"""
In this part of the tutorial we'll deliver a message to multiple consumers, being possible to
subscribe only to a subset of the messages. This pattern is known as "publish/subscribe" with routing.

    https://www.rabbitmq.com/tutorials/tutorial-four-python.html
"""

import sys
import pika


def main():
    # Open a connection with RabbitMQ server
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    # Create a 'direct_logs' exchange of type 'direct'
    channel.exchange_declare(exchange='direct_logs', exchange_type='direct')

    # Create the message to publish and its severity
    severity = sys.argv[1] if len(sys.argv) > 1 else 'info'
    message = ' '.join(sys.argv[2:]) or 'Hello World!'

    # Publish the message to the logs exchange
    channel.basic_publish(exchange='direct_logs', routing_key=severity, body=str.encode(message))
    print(" [x] Sent %r:%r" % (severity, message))

    # Close the connection
    connection.close()


# Main script
if __name__ == '__main__':
    main()
