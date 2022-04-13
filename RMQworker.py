# RMQ server -> 0.0.0.0:5672  || localhost:5672 
# Packages needed: PIKA
# Use this code only as a tool to get further comprehension about rabbitMQ
# This code is not, by anny matter, my property. 
# Its been taken, with educational purposes, from the following video.
# https://www.youtube.com/watch?v=Hy0cjAcxn_0&list=PLalrWAGybpB-UHbRDhFsBgXJM1g6T4IvO&index=12

# This version uses the pubsub scheme.

import pika as pk
import time
from pika.exchange_type import ExchangeType

rmqHost='localhost'
rmqPort=5672
exchBoard="pubsub"

def on_message_recieve(ch, method, properties, body):
    print(f"Recieved new message: {body}")
    ch.basic_ack(delivery_tag=method.delivery_tag) # Manual ack
    print("Finished processing")

connection_parameters = pk.ConnectionParameters(rmqHost,rmqPort)
connection = pk.BlockingConnection(connection_parameters)
channel = connection.channel()


# IMPORTANT
# This means that a worker will only process a petition at a time
channel.basic_qos(prefetch_count=1)

channel.exchange_declare(exchange=exchBoard, exchange_type=ExchangeType.fanout)

queue = channel.queue_declare(queue='', exclusive=True)

channel.queue_bind(exchange=exchBoard, queue=queue.method.queue)

# channel.basic_consume(queue=queueBoard, auto_ack=True, on_message_callback=on_message_recieve)
# We must remove the auto_ack=True parameter as we need to ack manually when the task is finished
channel.basic_consume(queue=queue.method.queue, on_message_callback=on_message_recieve)

print("Started consuming messages")

channel.start_consuming()