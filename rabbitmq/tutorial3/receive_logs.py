#!/usr/bin/env python

"""
In this part of the tutorial we'll deliver a message to multiple
consumers. This pattern is known as "publish/subscribe".

    https://www.rabbitmq.com/tutorials/tutorial-three-python.html
"""

import pika


def callback(ch, method, properties, body):
    print(" [x] %r" % body.decode("utf-8"))


def main():
    # Open a connection with RabbitMQ server
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    # Create a 'logs' exchange of type 'fanout'
    channel.exchange_declare(exchange='logs', exchange_type='fanout')

    # Create a queue to bind to the 'logs' exchange
    result = channel.queue_declare(queue='', exclusive=True)
    queue_name = result.method.queue

    # Indicate the exchange to send messages to the created queue (binding)
    channel.queue_bind(exchange='logs', queue=queue_name)

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
