import logging
from xmlrpc.client import boolean
from xmlrpc.server import SimpleXMLRPCServer

# Set up logging
server = SimpleXMLRPCServer(('localhost', 8000), logRequests=True, allow_none=True)
logging.basicConfig(level=logging.INFO)

workers_list = list()
added_servants = list() #Consistency
change = False #Global: https://www.w3schools.com/python/python_variables_global.asp

# Functions
def add_node(node):
    global change
    change = True
    added_servants.append(node)
    workers_list.append(node)

def remove_node(node):
    global change
    change = True
    workers_list.remove(node)

def get_workers():
    return workers_list

def get_added_servants():
    return added_servants

def get_has_changed():
    return change

def reset_change():
    global change
    change = False

server.register_function(add_node)
server.register_function(remove_node)
server.register_function(get_workers)
#Adding Consistency
server.register_function(get_has_changed)
server.register_function(reset_change)

# Start the server
try:
    print('Use Ctrl+c to exit')
    server.serve_forever()
except KeyboardInterrupt:
    print('Exiting')