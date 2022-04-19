#min max methods
import grpc
import pandas as pd
from concurrent import futures
import time

import gRPC_servant_pb2_grpc
import gRPC_servant_pb2

class gRPC_servant(gRPC_servant_pb2_grpc.gRPC_servantServicer):

    global df

    # Functions
    def read_csv(self, request, context):
        #global df
        #df = pd.read_csv(file)
        self.df = pd.read_csv(request.requestName)

    def max(self, request, context):
        #return str(df[axis].max())
        return gRPC_servant_pb2.Result(message = str(df[int(request.requestName)].max()))#incorrect int casting

    def min(self, request, context):
        #return str(df[axis].min())
        return 0

# create a gRPC server
server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

# use the generated function `add_CalculatorServicer_to_server`
# to add the defined class to the server
gRPC_servant_pb2_grpc.add_gRPC_servantServicer_to_server(
        gRPC_servant(), server)

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