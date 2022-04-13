# RMQ server -> 0.0.0.0:5672  || localhost:5672 
# Packages needed: PIKA
# This version does not implement publish subscribe scheme. 
# Use this code only as a tool to get further comprehension about rabbitMQ
# This code is not, by anny matter, my propperty. 
# Its been taken, with educational purposes, from the following video.
# https://www.youtube.com/watch?v=kwQDpHcM4HM&list=PLalrWAGybpB-UHbRDhFsBgXJM1g6T4IvO&index=4

import pika as pk

rmqHost='localhost'
rmqPort=5672

connection_parameters = pk.ConnectionParameters(rmqHost,rmqPort)
connection = pk.BlockingConnection(connection_parameters)
channel = connection.channel()

channel.queue_declare(queue='letterbox')

# Now that we have our queue set up we can publish a message.
# IMPORTANT NOTE!
# We don't ever publish a message directly to a queue, we must use the exchange.
# But to simplify we are going to use the default exchange

message = "Hello this is my first rabbit message"
channel.basic_publish(exchange='', routing_key='letterbox', body=message)
print("Message sent")
connection.close