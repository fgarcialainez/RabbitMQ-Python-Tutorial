#!/usr/bin/env python
import pika


def main():
    # Open a connection with RabbitMQ server
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    # Create a hello queue to which the message will be delivered
    channel.queue_declare(queue='hello')

    # Publish a message using the default exchange
    channel.basic_publish(exchange='', routing_key='hello', body=b'Hello World!')
    print(" [x] Sent 'Hello World!'")

    # Close the connection
    connection.close()


# Main script
if __name__ == '__main__':
    main()
