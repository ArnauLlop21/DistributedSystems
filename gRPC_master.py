from urllib import response
import grpc
from concurrent import futures
import time

import gRPC_master_pb2_grpc
import gRPC_master_pb2

class gRPC_master(gRPC_master_pb2_grpc.gRPC_masterServicer):
    #list
    workers_list = []

    # Functions
    def add_node(self, request, context):
        self.workers_list.append(str(request.requestNameMaster))
        return gRPC_master_pb2.ReturnedMessage(messageMaster="node added")

    def remove_node(self, request, context):
        self.workers_list.remove(str(request.requestNameMaster))
        return gRPC_master_pb2.ReturnedMessage(messageMaster="node removed")

    def get_workers(self, request, context):
        #response = gRPC_master_pb2.ListedServers()
        #response.listWorkers[:] = self.workers_list
        #return response
        return gRPC_master_pb2.ListedServers(listWorkers=self.workers_list)

# create a gRPC server
server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

# use the generated function `add_CalculatorServicer_to_server`
# to add the defined class to the server
gRPC_master_pb2_grpc.add_gRPC_masterServicer_to_server(
        gRPC_master(), server)

# listen on port 50051
print('Starting server. Listening on port 8000.')
server.add_insecure_port('[::]:8000')
server.start()

# since server.start() will not block,
# a sleep-loop is added to keep alive
try:
    while True:
        time.sleep(86400)
except KeyboardInterrupt:
    server.stop(0)