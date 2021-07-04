#!/usr/bin/env python

"""
In this part of the tutorial we'll deliver a message to multiple consumers, being possible to subscribe
only to a subset of them according to multiple criteria. This pattern is known as "topic" subscription.

    https://www.rabbitmq.com/tutorials/tutorial-five-python.html
"""

import sys
import pika


def main():
    # Open a connection with RabbitMQ server
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    # Create a 'topic_logs' exchange of type 'topic'
    channel.exchange_declare(exchange='topic_logs', exchange_type='topic')

    # Create the message to publish and its routing key
    routing_key = sys.argv[1] if len(sys.argv) > 2 else 'anonymous.info'
    message = ' '.join(sys.argv[2:]) or 'Hello World!'

    # Publish the message to the 'topic_logs' exchange
    channel.basic_publish(exchange='topic_logs', routing_key=routing_key, body=str.encode(message))
    print(" [x] Sent %r:%r" % (routing_key, message))

    # Close the connection
    connection.close()


# Main script
if __name__ == '__main__':
    main()
