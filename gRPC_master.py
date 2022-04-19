import grpc

class gRPC_master():
    #list
    workers_list = list()

    # Functions
    def add_node(self, node):
        self.workers_list.append(node)

    def remove_node(self, node):
        self.workers_list.remove(node)

    def get_workers(self):
        return self.workers_list



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