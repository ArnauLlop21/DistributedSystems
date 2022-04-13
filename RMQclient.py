# RMQ server -> 0.0.0.0:5672  || localhost:5672 

from email.base64mime import decodestring
import pika as pk
from pika.exchange_type import ExchangeType
import uuid
import pandas as pd
import time

rmqHost='localhost'
rmqPort=5672
exchBoard="pubsub"
replyQueue="replyqueue"
replyCache=[]
timeCache=[]

connection_parameters = pk.ConnectionParameters(rmqHost,rmqPort)
connection = pk.BlockingConnection(connection_parameters)
channel = connection.channel()

reply_queue=channel.queue_declare(queue=replyQueue, exclusive=True)

channel.exchange_declare(exchange=exchBoard, exchange_type=ExchangeType.fanout)

message = "titanic.csv;max;Age"
cor_id = str(uuid.uuid4())

channel.basic_publish(
    exchange=exchBoard, 
    routing_key='', 
    properties=pk.BasicProperties(
        reply_to=reply_queue.method.queue,
        correlation_id=cor_id,
        ),
    body=message)
print(f"Message sent: {message}")
live = True
timeOut=100
timeAct=0
timeIn=time.time()
while (live == True and timeOut > timeAct):

    method, properties, body = channel.basic_get(queue=reply_queue.method.queue, auto_ack=True)
    timeAct=time.time()-timeIn
    if body :
        answer=body.decode()
        answer=list(answer.split(";;;;"))
        replyCache.append(answer[0])
        timeCache.append(float(answer[1]))
        timeMax=max(timeCache)
        #print (timeMax)
        timeOut=5*timeMax
        #print (timeOut)

if list(message.split(";"))[1] == "max" or list(message.split(";"))[1] == "min":
    for i in range(0, len(replyCache)):
        replyCache[i] = float(replyCache[i])
    if list(message.split(";"))[1] == "max":
        print(max(replyCache))
    else:
        print(min(replyCache))
else:
    print(replyCache)

