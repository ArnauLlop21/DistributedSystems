import grpc

# import the generated classes (client/server/master)


# open a gRPC channel
channel = grpc.insecure_channel('localhost:9000')

# create a stub (client), proxy
stub = generatedClass.InsultAPIStub(channel)

response = stub.getInsults(InsultAPI_pb2.InsultListMessage())
response2 = stub.insultme(InsultAPI_pb2.Request())
response3 = stub.addInsult(InsultAPI_pb2.Request(requestName='cacota'))
# et voilà
print(response)
print(response2)
print(response3)