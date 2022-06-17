from doctest import master
from xmlrpc.client import ServerProxy
import pandas as pd
from socket import error as socketError
import redis
import time

# Redis implementation
redis_host = 'localhost'
redis_port = 6379

class Client:

    # Current workers list
    proxies = []
    # Redis instance
    r = redis.StrictRedis(host=redis_host, port=redis_port, decode_responses=True)
    # Gets current master
    masterP = r.get("master")
    
    # Inits master and workers list
    def __init__(self):
        self.master = ServerProxy('http://localhost:'+str(self.masterP), allow_none=True)
        self.create_proxys()
        self.master.reset_change()
    
    # Checks if master or workers list has changed, makes sure thre's consistency and fault tolerance
    def check_master_changed(self):
        messageIter = 0     # This variable only prevents the console from flooding
        # Prevents the client form communicatin to the old master 
        while (self.r.get("master_being_changed") == "True"):
            if (messageIter==0):
                print("The master is being changed.\nPlease, await so the operation can be carried away safely")
            if (messageIter%10 == 0):
                print("Wait a little bit more, please.\nWe're working on it!")
            messageIter+=1
            time.sleep(0.2)
        
        # Changes master if needed
        if(str(self.r.get("master")) != str(self.masterP)):      # If the port of the master has changed then
            print("Previous master was "+str(self.masterP)+"\nNew master is "+str(self.r.get("master")))
            self.masterP = self.r.get("master")
            self.master = ServerProxy('http://localhost:'+str(self.masterP), allow_none=True)
        # Changes workers list if needed
        if(self.master.get_has_changed()):
            self.create_proxys()
            self.master.reset_change()

    def create_proxys(self):
        workers_list = self.master.get_workers()
        # iterates over the list of workers and appends proxies of workers to client
        self.proxies.clear()
        for worker in workers_list:
            wk = ServerProxy(worker, allow_none=True)
            self.proxies.append(wk)

    def apply(self, cond, file):
        self.check_master_changed()
        #Loops through the current proxies and does apply, if client is not able to stablish connection returns an error code.
        aux=[]
        for current in self.proxies:
            aux.append(current.apply(str(cond), file))
        return aux

    def columns(self, file):
        self.check_master_changed()
        #Loops through the current proxies and does columns, if client is not able to stablish connection returns an error code.
        aux=[]
        for current in self.proxies:
            aux.append(current.columns(file))
        return aux
    
    def groupby(self, by, file):
        self.check_master_changed()
        #Loops through the current proxies and does groupby, if client is not able to stablish connection returns an error code.
        aux=[]
        for current in self.proxies:
            aux.append(current.groupby(by, file))
        return aux

    def head(self, n, file):
        self.check_master_changed()
        #Loops through the current proxies and does head, if client is not able to stablish connection returns an error code.
        aux=[]
        for current in self.proxies:
            aux.append(current.head(n, file))
        return aux

    def isin(self, val, file):
        self.check_master_changed()
        #Loops through the current proxies and does isin, if client is not able to stablish connection returns an error code.
        aux=[]
        for current in self.proxies:
            aux.append(current.isin(val, file))
        return aux
    
    def items(self, file):
        self.check_master_changed()
        #Loops through the current proxies and does items, if client is not able to stablish connection returns an error code.
        aux=[]
        for current in self.proxies:
            aux.append(current.items(file))
        return aux

    def max(self, axis, file):
        self.check_master_changed()
        #Loops through the current proxies and does max, if client is not able to stablish connection returns an error code.
        aux=[]
        for current in self.proxies:
            aux.append(current.max(axis, file))
        df = pd.DataFrame(aux);
        return df[0].max()
    
    def min(self, axis, file):
        self.check_master_changed()
        #Loops through the current proxies and does min, if client is not able to stablish connection returns an error code.
        aux=[]
        for current in self.proxies:
            aux.append(current.min(axis, file))
        df = pd.DataFrame(aux);
        return df[0].min()