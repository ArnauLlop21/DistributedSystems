#!/usr/bin/python
from concurrent.futures import thread
import logging
import random
import threading as thr
import time
import sys
from socket import error as socketError
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.client import ServerProxy
import pandas as pd
import redis

# Redis implementation
redis_host = 'localhost'
redis_port = 6379

r = redis.StrictRedis(host=redis_host, port=redis_port, decode_responses=True)

im_master = False
bullId = 0

# Set up logging for master, if master does not exist
if(sys.argv[1]=='0'):
    master_port = r.get("master")
    master = ServerProxy('http://localhost:'+str(master_port), allow_none=True)
    # Set up logging for Worker, if master exists
    server = SimpleXMLRPCServer(('localhost', int(sys.argv[2])), logRequests=True, allow_none=True)
    logging.basicConfig(level=logging.INFO)
    bullId = random.randint(0, sys.maxsize)
    print(bullId)
if(sys.argv[1]=='1'):
    # Inicialization of redis Master register
    r.set("master_being_changed" , str(False))
    r.set("master" , int(8000))
    server = SimpleXMLRPCServer(('localhost', int(r.get("master"))), logRequests=True, allow_none=True)
    im_master = True
    logging.basicConfig(level=logging.INFO)

workers_list = list()
change = False #Global: https://www.w3schools.com/python/python_variables_global.asp

file_name = "null"

# Functions Master
def set_lists(w_list):
    global workers_list
    workers_list = w_list.copy()

def add_node(node):
    global change, workers_list
    change = True
    workers_list.append(node)
    # Broadcast add_node -> setter for list and dictionary
    for worker in workers_list:
        proxy_current_wk = ServerProxy(worker, allow_none=True)
        proxy_current_wk.set_lists(workers_list)

def remove_node(node):
    global change, workers_list
    change = True
    workers_list.remove(node)
    # Broadcast remove_node -> setter for list and dictionary
    for worker in workers_list:
        proxy_current_wk = ServerProxy(worker, allow_none=True)
        proxy_current_wk.set_lists(workers_list)

def get_workers():
    return workers_list

def get_has_changed():
    return change

def reset_change():
    global change
    change = False

def check_workers():
    global change
    for worker in workers_list:
        try:
            ServerProxy(worker, allow_none=True).still_alive()
        except socketError:
            change = True
            remove_node(worker)
    time.sleep(0.1)

# Functions Workers
def turn_into_master(node):
    global im_master, master_port, change
    im_master = True
    change = True
    master_port = server.server_address[1] 
    r.set("master" , master_port)
    print("Luke, I am your master")
    remove_node(node)

#----- Bully protocol
def should_we_bully_you():
    global bullId
    return bullId

def lets_decide_who_to_bully():
    global workers_list
    minimumBull = [sys.maxsize, 0]
    for worker in workers_list:
        try:
            proxy = [ServerProxy(worker, allow_none=True).should_we_bully_you() , worker]
            if proxy[0] < minimumBull[0]: 
                minimumBull = proxy
        except socketError:
            print("Something has gone kaboom xd")
    return minimumBull[1]
#-----

def read_csv(file):
    global df
    global file_name
    file_name = file
    df = pd.read_csv(file)

def apply(cond, file):
    global df
    global file_name
    if(file != file_name):
        file_name = file
        df = pd.read_csv(file)
    return df.apply(eval(cond)).values.tolist()

def columns(file):
    global df
    global file_name
    if(file != file_name):
        file_name = file
        df = pd.read_csv(file)
    return df.columns.values.tolist()

def groupby(by, file):
    global df
    global file_name
    if(file != file_name):
        file_name = file
        df = pd.read_csv(file)
    return df.groupby(by).agg(['mean', 'count']).values.tolist()

def head(n, file):
    global df
    global file_name
    if(file != file_name):
        file_name = file
        df = pd.read_csv(file)
    return df.head(n).values.tolist()

def isin(val, file):
    global df
    global file_name
    if(file != file_name):
        file_name = file
        df = pd.read_csv(file)
    return df.isin(val).values.tolist()

def items(file):
    global df
    global file_name
    if(file != file_name):
        file_name = file
        df = pd.read_csv(file)
    aux=[]
    for label, content in df.items():
        aux.append(f'label:' + str(label))
        aux.append(f'content:' + str(content))
    return aux

def max(axis, file):
    global df
    global file_name
    if(file != file_name):
        file_name = file
        df = pd.read_csv(file)
    return str(df[axis].max())

def min(axis, file):
    global df
    global file_name
    if(file != file_name):
        file_name = file
        df = pd.read_csv(file)
    return str(df[axis].min())

def still_alive():
    return True

def check_master():
    global im_master, master_port
        #get current master using redis
    master_port = r.get("master")
    try:
        #checks if current master is alive
        ServerProxy('http://localhost:'+str(master_port), allow_none=True).get_has_changed()
    except socketError:
        #change first worker to master
        if(r.get("master_being_changed") == "False"):
            r.set("master_being_changed" , str(True))
            workerToBeBullied = lets_decide_who_to_bully()
            print("Father has failed us!")
            print("The worker "+str(workerToBeBullied)+" has been set to master")
            turn_into_master(str(workerToBeBullied))
            print("Correctly set")
            r.set("master_being_changed" , str(False))
        else:
            print("The change is being managed by another slave")
        
    time.sleep(0.1)

#Register Master Functions
server.register_function(add_node)
server.register_function(remove_node)
server.register_function(get_workers)
server.register_function(turn_into_master)

#Adding Consistency
server.register_function(set_lists)
server.register_function(get_has_changed)
server.register_function(reset_change)
server.register_function(check_workers)

#Register Workers Functions
server.register_function(read_csv)
server.register_function(apply)
server.register_function(columns)
server.register_function(groupby)
server.register_function(head)
server.register_function(isin)
server.register_function(items)
server.register_function(max)
server.register_function(min)
server.register_function(still_alive)
server.register_function(should_we_bully_you)

# Start the server
try:
    #Thread to start the server
    thread_serve = thr.Thread(target = server.serve_forever, daemon=True)
    thread_serve.start()
    
    if(sys.argv[1]=='0'):# Adds worker to master
        master.add_node('http://localhost:'+sys.argv[2])
    
    print('Use Ctrl+c to exit')
    while(True):
        if(im_master):# If we are Master, do master job -> check if workers still alive
            check_workers()
        else:# We are not master, so we do workers job -> check if master still alive
            check_master()
except KeyboardInterrupt:
    print('Exiting')