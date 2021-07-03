#!/usr/bin/env python
import pika


def callback(ch, method, properties, body):
    print(" [x] Received %r" % body.decode("utf-8"))


def main():
    # Open a connection with RabbitMQ server
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    # Create a hello queue to which the message will be delivered
    channel.queue_declare(queue='hello')

    # Receive messages from hello queue in callback function
    channel.basic_consume(queue='hello', on_message_callback=callback, auto_ack=True)

    # Enter a never-ending loop that waits for data and runs callbacks whenever necessary
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


# Main script
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('[*] Interrupted')
