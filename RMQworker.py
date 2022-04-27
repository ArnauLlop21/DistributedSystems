# RabbitMQ approach to server-client publish subscribe with reply request

import pika as pk
import time
from pika.exchange_type import ExchangeType
import pandas as pd
import RMQOptions as ro

rmqHost='localhost'
rmqPort=5672
exchBoard="pubsub"

def on_request_message_recieve(ch, method, properties, body):
    print("Recieved new message:",body, properties.correlation_id)
    startTime=time.time() # Starting the chrono
    petition=body.decode()
    petTpl=tuple(map(str, petition.split(";"))) # String into String tuple in order to manage information in an easier way
    toBeReported=str(workInPanditas(petTpl))    # Calculates the value to be returned. Strings it
    totalTime=str(time.time()-startTime)        
    reply = toBeReported+";;;;"+totalTime       # String to be reported back. It includes the message itself, a separator token and the time taken to calculate.
    ch.basic_publish('',routing_key=properties.reply_to, body=reply)
    print("Finished processing")

def workInPanditas(tuple):
    df=pd.read_csv(tuple[0])
    result=calculateSlave(df,tuple[1],str(tuple[2]))
    return result

def calculateSlave(df,option,parameter):    # Pandas' methods
    if parameter == "null" :
        #print("parameter null")
        if option == "columns":
            return ro.columns(df)
        elif option == "items":
            return ro.items(df)
        else: return "Something went wrong"
    else:
        #print("parameter not null")
        if option == "apply":
            return ro.apply(df,parameter)
        elif option == "groupby":
            return ro.groupby(df,parameter)
        elif option == "head":
            return ro.head(df, int(parameter))
        elif option == "isin":
            return ro.isin(df,parameter)
        elif option == "max":
            return ro.max(df,parameter)
        elif option == "min":
            return ro.min(df,parameter)
        else: return "Something went wrong"



connection_parameters = pk.ConnectionParameters(rmqHost,rmqPort)
connection = pk.BlockingConnection(connection_parameters)
channel = connection.channel()


# IMPORTANT
# This means that a worker will only process a petition at a time
channel.basic_qos(prefetch_count=1)

channel.exchange_declare(exchange=exchBoard, exchange_type=ExchangeType.fanout)
# The "empty" queue field forces the server to create a "random" instance of a unique queue
# This queue will be deleted as soon as it turns unused
queueSlave = channel.queue_declare(queue='', exclusive=True)
# Binding the specific queue created above to the broadcast exchange channel provided by the server
channel.queue_bind(exchange=exchBoard, queue=queueSlave.method.queue)
# Configuration for consuming the queue messages
channel.basic_consume(queue=queueSlave.method.queue, auto_ack=True, on_message_callback=on_request_message_recieve)

print("Started consuming messages")
# Endless loop. Fetches the messages inside the channelSlave
channel.start_consuming()