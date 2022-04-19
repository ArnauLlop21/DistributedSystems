import grpc

# import the generated classes (client/server/master)
import gRPC_servant_pb2_grpc
import gRPC_servant_pb2

# open a gRPC channel
channel = grpc.insecure_channel('localhost:9000')

# create a stub (client), proxy
stub = gRPC_servant_pb2_grpc.gRPC_servantStub(channel)

stub.read_csv(gRPC_servant_pb2.Request(requestName="titanic.csv"))
response = stub.max(gRPC_servant_pb2.Request(requestName="2"))
# et voilà
print(response)