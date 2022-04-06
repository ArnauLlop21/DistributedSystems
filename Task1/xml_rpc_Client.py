from xmlrpc.client import ServerProxy
import pandas as pd

class Client:

    def __init__(self):
        master = ServerProxy('http://localhost:8000', allow_none=True)
        workers_list = master.get_workers()
        # iterates over the list and appends workers to client
        self.proxies = []
        for worker in workers_list:
            wk = ServerProxy(worker, allow_none=True)
            self.proxies.append(wk)
    
    def read_csv(self, name):
        for current in self.proxies:
            current.read_csv(name)

    def apply(self, cond):
        aux=[]
        for current in self.proxies:
            aux.append(current.apply(str(cond)))
        return aux

    def columns(self):
        aux=[]
        for current in self.proxies:
            aux.append(current.columns())
        return aux
    
    def groupby(self, by):
        aux=[]
        for current in self.proxies:
            aux.append(current.groupby(by))
        return aux

    def head(self, n):
        aux=[]
        for current in self.proxies:
            aux.append(current.head(n))
        return aux

    def isin(self, val):
        aux=[]
        for current in self.proxies:
            aux.append(current.isin(val))
        return aux
    
    def items(self):
        aux=[]
        for current in self.proxies:
            aux.append(current.items())
        return aux

    def max(self):
        aux=[]
        for current in self.proxies:
            aux.append(current.max())
        return aux
    
    def min(self, axis):
        aux=[]
        for current in self.proxies:
            aux.append(current.min(axis))
        return aux
#Main:
client1 = Client()
client1.read_csv("cities.csv")
#print(client1.apply("[1, 2], axis=1"))Problemes
#print(client1.columns())
#print(client1.groupby(["PassengerId"]))
#print(client1.head(5))
#print(client1.isin([41, 80]))
#print(client1.items())
#print(client1.min("axis=0"))
print(client1.max())