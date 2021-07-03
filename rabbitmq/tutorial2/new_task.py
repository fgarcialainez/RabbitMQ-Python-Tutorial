#!/usr/bin/env python

"""
In this tutorial we'll create a Work Queue that will be used to
distribute time-consuming tasks among multiple workers.

    https://www.rabbitmq.com/tutorials/tutorial-two-python.html
"""

import sys
import pika


def main():
    # Open a connection with RabbitMQ server
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    # Create a 'task_queue' queue to which the message will be delivered
    channel.queue_declare(queue='task_queue', durable=True)

    # Create the message from the user input
    message = ' '.join(sys.argv[1:]) or "Hello World!"

    # Publish a message using the default exchange
    channel.basic_publish(
        exchange='',
        routing_key='task_queue',
        body=str.encode(message),
        properties=pika.BasicProperties(
            delivery_mode=2,  # make message persistent
        ))

    print(" [x] Sent %r" % message)

    # Close the connection
    connection.close()


# Main script
if __name__ == '__main__':
    main()
