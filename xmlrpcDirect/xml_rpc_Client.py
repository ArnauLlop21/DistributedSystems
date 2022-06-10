from xmlrpc.client import ServerProxy
import pandas as pd

class Client:

    proxies = []

    def __init__(self):
        self.master = ServerProxy('http://localhost:8000', allow_none=True)
        self.create_proxys()
        self.master.reset_change()

    def create_proxys(self):
        workers_list = self.master.get_workers()
        # iterates over the list and appends workers to client
        self.proxies.clear()
        for worker in workers_list:
            wk = ServerProxy(worker, allow_none=True)
            self.proxies.append(wk)

    def apply(self, cond, file):
        #Maintain consistency
        if(self.master.get_has_changed()):
            self.create_proxys()
            self.master.reset_change()

        aux=[]
        for current in self.proxies:
            aux.append(current.apply(str(cond), file))
        return aux

    def columns(self, file):
        #Maintain consistency
        if(self.master.get_has_changed()):
            self.create_proxys()
            self.master.reset_change()

        aux=[]
        for current in self.proxies:
            aux.append(current.columns(file))
        return aux
    
    def groupby(self, by, file):
        #Maintain consistency
        if(self.master.get_has_changed()):
            self.create_proxys()
            self.master.reset_change()

        aux=[]
        for current in self.proxies:
            aux.append(current.groupby(by, file))
        return aux

    def head(self, n, file):
        #Maintain consistency
        if(self.master.get_has_changed()):
            self.create_proxys()
            self.master.reset_change()

        aux=[]
        for current in self.proxies:
            aux.append(current.head(n, file))
        return aux

    def isin(self, val, file):
        #Maintain consistency
        if(self.master.get_has_changed()):
            self.create_proxys()
            self.master.reset_change()

        aux=[]
        for current in self.proxies:
            aux.append(current.isin(val, file))
        return aux
    
    def items(self, file):
        #Maintain consistency
        if(self.master.get_has_changed()):
            self.create_proxys()
            self.master.reset_change()

        aux=[]
        for current in self.proxies:
            aux.append(current.items(file))
        return aux

    def max(self, axis, file):
        #Maintain consistency
        if(self.master.get_has_changed()):
            self.create_proxys()
            self.master.reset_change()

        aux=[]
        for current in self.proxies:
            aux.append(current.max(axis, file))
        df = pd.DataFrame(aux);
        return df[0].max()
    
    def min(self, axis, file):
        #Maintain consistency
        if(self.master.get_has_changed()):
            self.create_proxys()
            self.master.reset_change()

        aux=[]
        for current in self.proxies:
            aux.append(current.min(axis, file))
        df = pd.DataFrame(aux);
        return df[0].min()
#Main:
client1 = Client()
print(client1.proxies)
print(client1.apply("lambda x: x + x", "titanic.csv"))
print(client1.columns("titanic.csv"))
input()
print(client1.groupby(["PassengerId"], "titanic.csv"))
print(client1.proxies)
print(client1.head(5, "titanic.csv"))
print(client1.head(5, "titanic.csv"))
print(client1.isin([41, 80], "titanic.csv"))
print(client1.items("titanic.csv"))
print(client1.min("PassengerId", "titanic.csv"))
print(client1.max("PassengerId", "titanic.csv"))