#!/usr/bin/env python

"""
In this tutorial we're going to use RabbitMQ to build an RPC system: a client and a scalable RPC server.

    https://www.rabbitmq.com/tutorials/tutorial-six-python.html
"""

import pika


def fib(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib(n - 1) + fib(n - 2)


def on_request(ch, method, props, body):
    n = int(body)

    print(" [.] fib(%s)" % n)
    response = fib(n)

    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id=props.correlation_id),
                     body=str(response))
    ch.basic_ack(delivery_tag=method.delivery_tag)


def main():
    # Open a connection with RabbitMQ server
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    # Create a 'rpc_queue' queue from which the messages will be received
    channel.queue_declare(queue='rpc_queue')

    # Receive messages from 'rpc_queue' queue in the callback function
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='rpc_queue', on_message_callback=on_request)

    # Enter a never-ending loop that waits for data and runs callbacks whenever necessary
    print(" [x] Awaiting RPC requests")
    channel.start_consuming()


# Main script
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('[*] Interrupted')
