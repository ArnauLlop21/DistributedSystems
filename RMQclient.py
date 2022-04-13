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
import random as rd
import time
rmqHost='localhost'
rmqPort=5672
queueBoard='letterbox'

connection_parameters = pk.ConnectionParameters(rmqHost,rmqPort)
connection = pk.BlockingConnection(connection_parameters)
channel = connection.channel()

channel.queue_declare(queue=queueBoard)

# Now that we have our queue set up we can publish a message.
# IMPORTANT NOTE!
# We don't ever publish a message directly to a queue, we must use the exchange.
# But to simplify we are going to use the default exchange

petID=0
while (True):
    message = f"Petition number: {petID}"
    channel.basic_publish(exchange='', routing_key=queueBoard, body=message)
    print("Message sent")
    petID += 1
    time.sleep(rd.randint(1,3))
