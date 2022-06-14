#!/usr/bin/python
from concurrent.futures import thread
import logging
import threading as thr
import time
from socket import error as socketError
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.client import ServerProxy

# Set up logging
server = SimpleXMLRPCServer(('localhost', 8000), logRequests=True, allow_none=True)
logging.basicConfig(level=logging.INFO)

workers_list = list()
worker_proxy = {}
change = False #Global: https://www.w3schools.com/python/python_variables_global.asp

# Functions
def add_node(node):
    global change
    change = True
    workers_list.append(node)
    worker_proxy[node] = ServerProxy(node, allow_none=True)

def remove_node(node):
    global change
    change = True
    workers_list.remove(node)
    worker_proxy.pop(node)

def get_workers():
    return workers_list

def get_has_changed():
    return change

def reset_change():
    global change
    change = False

def check_workers():
    global change
    for worker in worker_proxy:
        try:
            worker_proxy.get(worker).still_alive()
        except socketError:
            change = True
            remove_node(worker)
    time.sleep(0.1)


server.register_function(add_node)
server.register_function(remove_node)
server.register_function(get_workers)
#Adding Consistency
server.register_function(get_has_changed)
server.register_function(reset_change)

# Start the server
try:
    print('Use Ctrl+c to exit')
    thread1 = thr.Thread(target = check_workers)
    thread1.start()
    server.serve_forever()
except KeyboardInterrupt:
    print('Exiting')