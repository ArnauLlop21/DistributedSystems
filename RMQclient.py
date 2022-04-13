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

def on_message_recieve(ch, method, properties, body):
    print(f"Recieved new message: {body}")

connection_parameters = pk.ConnectionParameters(rmqHost,rmqPort)
connection = pk.BlockingConnection(connection_parameters)
channel = connection.channel()

# It is mostly okay to declare the same queue more than once 
# as rabbitmq will only execute the first instance of it.
channel.queue_declare(queue='letterbox')

channel.basic_consume(queue='letterbox', auto_ack=True, on_message_callback=on_message_recieve)

print("Started consuming messages")

channel.start_consuming()