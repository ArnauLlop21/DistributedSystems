# RMQ server -> 0.0.0.0:5672  || localhost:5672 
# Packages needed: PIKA
# This version does not implement publish subscribe scheme. 
# Use this code only as a tool to get further comprehension about rabbitMQ
# This code is not, by anny matter, my property. 
# Its been taken, with educational purposes, from the following video.
# https://www.youtube.com/watch?v=hi8DjlcbN4A&list=PLalrWAGybpB-UHbRDhFsBgXJM1g6T4IvO&index=8
# https://www.youtube.com/watch?v=jXBd0jP6EoE&list=PLalrWAGybpB-UHbRDhFsBgXJM1g6T4IvO&index=9

# This version uses the competing worker scheme. NOT TO BE USED in the assignment.
# Educational purposes

import pika as pk
import time

rmqHost='localhost'
rmqPort=5672
queueBoard='letterbox'

def on_message_recieve(ch, method, properties, body):
    print(f"Recieved new message: {body}")
    time.sleep(4) # This is to simulate a task being processed for the sake of this example
    ch.basic_ack(delivery_tag=method.delivery_tag) # Manual ack
    print("Finished processing")

connection_parameters = pk.ConnectionParameters(rmqHost,rmqPort)
connection = pk.BlockingConnection(connection_parameters)
channel = connection.channel()

# It is mostly okay to declare the same queue more than once 
# as rabbitmq will only execute the first instance of it.
channel.queue_declare(queue=queueBoard)

# IMPORTANT
# This means that a worker will only process a petition at a time
channel.basic_qos(prefetch_count=1)

# channel.basic_consume(queue=queueBoard, auto_ack=True, on_message_callback=on_message_recieve)
# We must remove the auto_ack=True parameter as we need to ack manually when the task is finished
channel.basic_consume(queue=queueBoard, on_message_callback=on_message_recieve)

print("Started consuming messages")

channel.start_consuming()