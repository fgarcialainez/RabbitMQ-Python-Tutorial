#!/usr/bin/env python

"""
In this part of the tutorial we'll deliver a message to multiple consumers, being possible to
subscribe only to a subset of the messages. This pattern is known as "publish/subscribe" with routing.

    https://www.rabbitmq.com/tutorials/tutorial-four-python.html
"""

import sys
import pika


def callback(ch, method, properties, body):
    print(" [x] %r:%r" % (method.routing_key, body.decode("utf-8")))


def main():
    # Open a connection with RabbitMQ server
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    # Create a 'direct_logs' exchange of type 'direct'
    channel.exchange_declare(exchange='direct_logs', exchange_type='direct')

    # Create a queue to bind to the 'direct_logs' exchange
    result = channel.queue_declare(queue='', exclusive=True)
    queue_name = result.method.queue

    # Get the severities from the args list
    severities = sys.argv[1:]

    if not severities:
        sys.stderr.write("Usage: %s [info] [warning] [error]\n" % sys.argv[0])
        sys.exit(1)

    # Create a binding for each severity
    for severity in severities:
        # Indicate the exchange to send messages with the given severity to the created queue (binding)
        channel.queue_bind(exchange='direct_logs', queue=queue_name, routing_key=severity)

    # Receive messages from the queue in callback function
    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

    # Enter a never-ending loop that waits for data and runs callbacks whenever necessary
    print(' [*] Waiting for logs. To exit press CTRL+C')
    channel.start_consuming()


# Main script
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('[*] Interrupted')
