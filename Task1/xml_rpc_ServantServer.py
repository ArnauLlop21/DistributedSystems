import logging
from xmlrpc.client import ServerProxy
from xmlrpc.server import SimpleXMLRPCServer
import pandas as pd

port = 9000

# Set up logging
worker = SimpleXMLRPCServer(('localhost', port), logRequests=True, allow_none=True)
logging.basicConfig(level=logging.INFO)

master = ServerProxy('http://localhost:8000', allow_none=True)

# Functions
def read_csv(file):
    global df
    df = pd.read_csv(file)

def apply(func):
    return df.apply(func).values.tolist()

def columns():
    return df.columns.values.tolist()

def groupby(by):
    return df.groupby(by).values.tolist()

def head(n):
    return df.head(n).values.tolist()

def isin(val):
    return df.isin(val).values.tolist()

def items():
    return df.items().values.tolist()

def max(axis):
    return df.max(axis).values.tolist()

def min(axis):
    return df.min(axis).values.tolist()

worker.register_function(read_csv)
worker.register_function(apply)
worker.register_function(columns)
worker.register_function(groupby)
worker.register_function(head)
worker.register_function(isin)
worker.register_function(items)
worker.register_function(max)
worker.register_function(min)

# Start the server
try:
    print('Use Ctrl+c to exit')
    master.add_node('http://localhost:'+str(port))
    worker.serve_forever()
except KeyboardInterrupt:
    print('Exiting')