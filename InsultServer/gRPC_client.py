from ast import In
from email import message
import grpc

# import the generated classes
import InsultAPI_pb2_grpc
import InsultAPI_pb2

# open a gRPC channel
channel = grpc.insecure_channel('localhost:50051')

# create a stub (client), proxy
stub = InsultAPI_pb2_grpc.InsultAPIStub(channel)

response = stub.getInsults(InsultAPI_pb2.InsultListMessage())
response2 = stub.insultme(InsultAPI_pb2.Request())
response3 = stub.addInsult(InsultAPI_pb2.Request(requestName='cacota'))
# et voilà
print(response)
print(response2)
print(response3)