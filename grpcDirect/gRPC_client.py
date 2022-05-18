import grpc

# import the generated classes (client/server/master)
import gRPC_servant_pb2_grpc
import gRPC_servant_pb2
import gRPC_master_pb2_grpc
import gRPC_master_pb2
import pandas as pd

class Client:

    def __init__(self):
        # open a gRPC channel to master
        channel = grpc.insecure_channel('localhost:8000')
        # create a stub client to master, proxy
        stub = gRPC_master_pb2_grpc.gRPC_masterStub(channel)
        workers_list = str(stub.get_workers(gRPC_master_pb2.RequestMaster()))
        splittedWorkers = workers_list.splitlines()
        self.proxies = []
        for splitwk in splittedWorkers:
            aux=splitwk.split(" ")
            aux[1] = str(aux[1]).removeprefix('"').removesuffix('"')
            channel = grpc.insecure_channel(aux[1])
            stub = gRPC_servant_pb2_grpc.gRPC_servantStub(channel)
            self.proxies.append(stub)
    
    def read_csv(self, name):
        for current in self.proxies:
            print(current.read_csv(gRPC_servant_pb2.Request(requestName=name)))

    def max(self, axis):
        aux=[]
        for current in self.proxies:
            aux.append(current.max(gRPC_servant_pb2.Request(requestName=axis)).message)
        df = pd.DataFrame(aux);
        return df[0].max()
    
    def min(self, axis):
        aux=[]
        for current in self.proxies:
            aux.append(current.min(gRPC_servant_pb2.Request(requestName=axis)).message)
        df = pd.DataFrame(aux);
        return df[0].min()
#Main:
client1 = Client()
client1.read_csv("titanic.csv")
print(client1.max("PassengerId"))
print(client1.min("PassengerId"))