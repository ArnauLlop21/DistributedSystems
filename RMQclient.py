# RabbitMQ approach to server-client publish subscribe with reply request

from email.base64mime import decodestring
import pika as pk
from pika.exchange_type import ExchangeType
import uuid
import pandas as pd
import time

# Global configuration information
rmqHost='localhost'
rmqPort=5672
exchBoard="pubsub"
replyQueue="replyqueue"

# Global variables 
replyCache=[]
timeCache=[]

# Petition message.
# Special format required:
# str(fileToBeRead;operationToBeApplied;paramNeeded)
# If no parameter is needed leave the third field as "null"
# message = "titanic.csv;head;5"
# message = "titanic.csv;columns;null"
message = "titanic.csv;columns;null"

# Connection configuration
connection_parameters = pk.ConnectionParameters(rmqHost,rmqPort)
connection = pk.BlockingConnection(connection_parameters)
channel = connection.channel()
reply_queue=channel.queue_declare(queue=replyQueue, exclusive=True)
channel.exchange_declare(exchange=exchBoard, exchange_type=ExchangeType.fanout) # Creates the fanout (broadcast) exchange
cor_id = str(uuid.uuid4())                                                      # Formality, not really used
channel.basic_publish(
    exchange=exchBoard, 
    routing_key='', 
    properties=pk.BasicProperties(
        reply_to=reply_queue.method.queue,
        correlation_id=cor_id,
        ),
    body=message)

#print(f"Message sent: {message}")

# Variables in charge of controlling the while loop
timeOut=100     # Arbitrary maximum time. Set so the client wont be waiting more than 100sec for an answer
timeAct=0
timeIn=time.time()

# This loop goes through until the maximum permitted time is exceeded
while (timeOut >= timeAct):
    # This line retrieves the information inside the reply_queue if existing.
    # Gets "None" otherwise
    method, properties, body = channel.basic_get(queue=reply_queue.method.queue, auto_ack=True)
    timeAct=time.time()-timeIn
    if body :
        answer=body.decode()                    # Decodes the byte answer into a string.
        answer=list(answer.split(";;;;"))       # Splits the string and creates and array with it
        replyCache.append(answer[0])            # Saves the replies for further management
        timeCache.append(float(answer[1]))      # Saves the times on the replies for further management
        timeMax=max(timeCache)
        timeOut=5*timeMax                       # The maximum time to be waited is five times the maximum waiting time of the slaves

if list(message.split(";"))[1] == "max" or list(message.split(";"))[1] == "min":
    for i in range(0, len(replyCache)):
        replyCache[i] = float(replyCache[i])
    if list(message.split(";"))[1] == "max":
        print(max(replyCache))                  # If the answer is purely numeric then print the applied operation of all the answers
    else:
        print(min(replyCache))
else:
    print(replyCache)                           # Else then print all the answers

