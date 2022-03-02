import grpc

# import the generated classes
import InsultAPI_pb2_grpc
import InsultAPI_pb2

# open a gRPC channel
channel = grpc.insecure_channel('localhost:50051')

# create a stub (client)
stub = InsultAPI_pb2_grpc.InsultAPIStub(channel)

# create a valid request message
number = []
number = InsultAPI_pb2.Insults()

# make the call
response = stub.getInsults(number)

# et voilà
print(response)