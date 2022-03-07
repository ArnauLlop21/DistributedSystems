# pip install grpcio
# pip install grpcio-tools
from email import message
from unicodedata import name
from urllib import response
import grpc
from concurrent import futures
import time
import random

import InsultAPI_pb2_grpc
import InsultAPI_pb2

class insultsAPI(InsultAPI_pb2_grpc.InsultAPIServicer):

    insultList = []

    def __init__(self):
        insultFile = open("InsultList.txt", 'r')
        for line in insultFile:
            insultsAPI.insultList.append(line)     #line.strip
        insultFile.close()

    def getInsults(self, request, context):
        return InsultAPI_pb2.InsultListMessage(list=insultsAPI.insultList)
    
    def insultme(self, request, context):
        return InsultAPI_pb2.RandInsultMessage(message=insultsAPI.insultList[random.randint(0, len(insultsAPI.insultList)-1)])

    def addInsult(self, request, context):
        insultsAPI.insultList.append(str(request.requestName))
        insultFile = open("InsultList.txt", 'a')
        insultFile.write("\n")
        insultFile.write(str(request.requestName))
        insultFile.close()
        return InsultAPI_pb2.RandInsultMessage(message=("Insult added! "+str(request.requestName)))

# create a gRPC server
server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

# use the generated function `add_CalculatorServicer_to_server`
# to add the defined class to the server
InsultAPI_pb2_grpc.add_InsultAPIServicer_to_server(
        insultsAPI(), server)

# listen on port 50051
print('Starting server. Listening on port 50051.')
server.add_insecure_port('[::]:50051')
server.start()

# since server.start() will not block,
# a sleep-loop is added to keep alive
try:
    while True:
        time.sleep(86400)
except KeyboardInterrupt:
    server.stop(0)