import logging
import sys
from xmlrpc.client import ServerProxy
from xmlrpc.server import SimpleXMLRPCServer
import pandas as pd

port = 9001

# Set up logging
worker = SimpleXMLRPCServer(('localhost', port), logRequests=True, allow_none=True)
logging.basicConfig(level=logging.INFO)

master = ServerProxy('http://localhost:8000', allow_none=True)

file_name = "null"

# Functions
def read_csv(file):
    global df
    global file_name
    file_name = file
    df = pd.read_csv(file)
#func casting string to server -> eval()
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

#Check if master still alive
worker.register_function(read_csv)
worker.register_function(apply)
worker.register_function(columns)
worker.register_function(groupby)
worker.register_function(head)
worker.register_function(isin)
worker.register_function(items)
worker.register_function(max)
worker.register_function(min)
worker.register_function(still_alive)

# Start the server
try:
    print('Use Ctrl+c to exit')
    master.add_node('http://localhost:'+str(port))
    worker.serve_forever()
except KeyboardInterrupt:
    master.remove_node('http://localhost:'+str(port))
    print('Exiting')