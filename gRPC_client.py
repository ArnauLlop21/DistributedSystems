import grpc

# import the generated classes (client/server/master)
import gRPC_servant_pb2_grpc
import gRPC_servant_pb2
import gRPC_master_pb2_grpc
import gRPC_master_pb2

# open a gRPC channel
channel = grpc.insecure_channel('localhost:8000')

# create a stub (client), proxy
stub = gRPC_master_pb2_grpc.gRPC_masterStub(channel)
workers_list = list()
workers_list[:] = stub.get_workers(gRPC_master_pb2.RequestMaster())

for wk in workers_list:
    print(wk)

#print(stub.read_csv(gRPC_servant_pb2.Request(requestName="titanic.csv")))
#response1 = stub.max(gRPC_servant_pb2.Request(requestName="PassengerId"))
#response2 = stub.min(gRPC_servant_pb2.Request(requestName="PassengerId"))
# et voilà
#print(response1)
#print(response2)