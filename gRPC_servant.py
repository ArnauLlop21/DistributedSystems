#min max methods
import grpc
import pandas as pd
from concurrent import futures
import time

import gRPC_servant_pb2_grpc
import gRPC_servant_pb2

port = 9001

class gRPC_servant(gRPC_servant_pb2_grpc.gRPC_servantServicer):

    # Functions
    def read_csv(self, request, context):
        self.df = pd.read_csv(request.requestName)
        return gRPC_servant_pb2.Result(message="csv!")

    def max(self, request, context):
        return gRPC_servant_pb2.Result(message = str(self.df[request.requestName].max()))

    def min(self, request, context):
        return gRPC_servant_pb2.Result(message = str(self.df[request.requestName].min()))

# create a gRPC server
server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

# use the generated function `add_CalculatorServicer_to_server`
# to add the defined class to the server
gRPC_servant_pb2_grpc.add_gRPC_servantServicer_to_server(
        gRPC_servant(), server)

# listen on port
print('Starting server. Listening on port '+str(port))
server.add_insecure_port('[::]:'+str(port))
server.start()

import gRPC_master_pb2_grpc
import gRPC_master_pb2
# open a gRPC channel to master
channel = grpc.insecure_channel('localhost:8000')
# create a stub servant to master proxy
stub = gRPC_master_pb2_grpc.gRPC_masterStub(channel)
# add servant to master
stub.add_node(gRPC_master_pb2.ReturnedMessage(messageMaster='localhost:'+str(port)))
# -------

# since server.start() will not block,
# a sleep-loop is added to keep alive
try:
    while True:
        time.sleep(86400)
except KeyboardInterrupt:
    # deleting servant from master
    stub.remove_node(gRPC_master_pb2.RequestMaster(requestNameMaster='localhost:'+str(port)))
    server.stop(0)