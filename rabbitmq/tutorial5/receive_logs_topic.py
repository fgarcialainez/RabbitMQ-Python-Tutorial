#!/usr/bin/env python

"""
In this part of the tutorial we'll deliver a message to multiple consumers, being possible to subscribe
only to a subset of them according to multiple criteria. This pattern is known as "topic" subscription.

    https://www.rabbitmq.com/tutorials/tutorial-five-python.html
"""

import sys
import pika


def callback(ch, method, properties, body):
    print(" [x] %r:%r" % (method.routing_key, body.decode("utf-8")))


def main():
    # Open a connection with RabbitMQ server
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    # Create a 'topic_logs' exchange of type 'topic'
    channel.exchange_declare(exchange='topic_logs', exchange_type='topic')

    # Create a queue to bind to the 'topic_logs' exchange
    result = channel.queue_declare(queue='', exclusive=True)
    queue_name = result.method.queue

    # Get the binding keys from the args list
    binding_keys = sys.argv[1:]

    if not binding_keys:
        sys.stderr.write("Usage: %s [binding_key]...\n" % sys.argv[0])
        sys.exit(1)

    # Create a binding for each binding key
    for binding_key in binding_keys:
        # Indicate the exchange to send messages with the given binding key to the created queue (binding)
        channel.queue_bind(exchange='topic_logs', queue=queue_name, routing_key=binding_key)

    # Receive messages from the queue in the callback function
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
