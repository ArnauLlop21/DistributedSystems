# RMQ server -> 0.0.0.0:5672  || localhost:5672 
# Packages needed: PIKA
# Use this code only as a tool to get further comprehension about rabbitMQ
# This code is not, by anny matter, my property. 
# Its been taken, with educational purposes, from the following video.
# https://www.youtube.com/watch?v=Hy0cjAcxn_0&list=PLalrWAGybpB-UHbRDhFsBgXJM1g6T4IvO&index=12

# This version uses the pubsub scheme.

import pika as pk
import random as rd
import time
from pika.exchange_type import ExchangeType

rmqHost='localhost'
rmqPort=5672
queueBoard='letterbox'
exchBoard="pubsub"

connection_parameters = pk.ConnectionParameters(rmqHost,rmqPort)
connection = pk.BlockingConnection(connection_parameters)
channel = connection.channel()

channel.exchange_declare(exchange=exchBoard, exchange_type=ExchangeType.fanout)

# Now that we have our queue set up we can publish a message.
# IMPORTANT NOTE!
# We don't ever publish a message directly to a queue, we must use the exchange.
# But to simplify we are going to use the default exchange

message = f"Message to be broadcasted"
channel.basic_publish(exchange=exchBoard, routing_key='', body=message)
print(f"Message sent: {message}")
connection.close()

