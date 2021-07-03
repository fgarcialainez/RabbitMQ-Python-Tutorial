#!/usr/bin/env python

"""
In this tutorial we'll create a Work Queue that will be used to
distribute time-consuming tasks among multiple workers.

    https://www.rabbitmq.com/tutorials/tutorial-two-python.html
"""

import pika
import time


def callback(ch, method, properties, body):
    # Sleep the thread
    print(" [x] Received %r" % body.decode("utf-8"))
    time.sleep(body.count(b'.'))
    print(" [x] Done")

    # Send ACK
    ch.basic_ack(delivery_tag=method.delivery_tag)


def main():
    # Open a connection with RabbitMQ server
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    # Create a 'task_queue' from which the messages will received
    channel.queue_declare(queue='task_queue', durable=True)

    # Dispatch messages evenly (fair dispatch). Don't dispatch a new message
    # to a worker until it has processed and acknowledged the previous one
    channel.basic_qos(prefetch_count=1)

    # Receive messages from 'task_queue' queue in callback function
    channel.basic_consume(queue='task_queue', on_message_callback=callback)

    # Enter a never-ending loop that waits for data and runs callbacks whenever necessary
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


# Main script
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('[*] Interrupted')