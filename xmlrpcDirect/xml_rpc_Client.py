from xmlrpc.client import ServerProxy
import pandas as pd
from socket import error as socketError

class Client:

    proxies = []

    def __init__(self):
        self.master = ServerProxy('http://localhost:8000', allow_none=True)
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
        #Maintain consistency
        if(self.master.get_has_changed()):
            self.create_proxys()
            self.master.reset_change()
        #Loops through the current proxies and does apply, if client is not able to stablish connection returns an error code.
        aux=[]
        for current in self.proxies:
            try:
                aux.append(current.apply(str(cond), file))
            except socketError:
                aux.append("Cannot communicate to: " + str(current))
        return aux

    def columns(self, file):
        #Maintain consistency
        if(self.master.get_has_changed()):
            self.create_proxys()
            self.master.reset_change()
        #Loops through the current proxies and does columns, if client is not able to stablish connection returns an error code.
        aux=[]
        for current in self.proxies:
            try:
                aux.append(current.columns(file))
            except socketError:
                aux.append("Cannot communicate to: " + str(current))
        return aux
    
    def groupby(self, by, file):
        #Maintain consistency
        if(self.master.get_has_changed()):
            self.create_proxys()
            self.master.reset_change()
        #Loops through the current proxies and does groupby, if client is not able to stablish connection returns an error code.
        aux=[]
        for current in self.proxies:
            try:
                aux.append(current.groupby(by, file))
            except socketError:
                aux.append("Cannot communicate to: " + str(current))
        return aux

    def head(self, n, file):
        #Maintain consistency
        if(self.master.get_has_changed()):
            self.create_proxys()
            self.master.reset_change()
        #Loops through the current proxies and does head, if client is not able to stablish connection returns an error code.
        aux=[]
        for current in self.proxies:
            try:
                aux.append(current.head(n, file))
            except socketError:
                aux.append("Cannot communicate to: " + str(current))
        return aux

    def isin(self, val, file):
        #Maintain consistency
        if(self.master.get_has_changed()):
            self.create_proxys()
            self.master.reset_change()
        #Loops through the current proxies and does isin, if client is not able to stablish connection returns an error code.
        aux=[]
        for current in self.proxies:
            try:
                aux.append(current.isin(val, file))
            except socketError:
                aux.append("Cannot communicate to: " + str(current))
        return aux
    
    def items(self, file):
        #Maintain consistency
        if(self.master.get_has_changed()):
            self.create_proxys()
            self.master.reset_change()
        #Loops through the current proxies and does items, if client is not able to stablish connection returns an error code.
        aux=[]
        for current in self.proxies:
            try:
                aux.append(current.items(file))
            except socketError:
                aux.append("Cannot communicate to: " + str(current))
        return aux

    def max(self, axis, file):
        #Maintain consistency
        if(self.master.get_has_changed()):
            self.create_proxys()
            self.master.reset_change()
        #Loops through the current proxies and does max, if client is not able to stablish connection returns an error code.
        aux=[]
        for current in self.proxies:
            try:
                aux.append(current.max(axis, file))
            except socketError:
                aux.append("Cannot communicate to: " + str(current))
        df = pd.DataFrame(aux);
        return df[0].max()
    
    def min(self, axis, file):
        #Maintain consistency
        if(self.master.get_has_changed()):
            self.create_proxys()
            self.master.reset_change()
        #Loops through the current proxies and does min, if client is not able to stablish connection returns an error code.
        aux=[]
        for current in self.proxies:
            try:
                aux.append(current.min(axis, file))
            except socketError:
                aux.append("Cannot communicate to: " + str(current))
        df = pd.DataFrame(aux);
        return df[0].min()
#Main:
#client1 = Client()
#print(client1.proxies)
'''
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
'''

#print(client1.min("PassengerId", "titanic.csv"))

master = ServerProxy('http://localhost:8000', allow_none=True)
print(master.get_workers())
print(master.isin([41, 80], "titanic.csv"))
print(master.items("titanic.csv"))
print(master.min("PassengerId", "titanic.csv"))
print(master.max("PassengerId", "titanic.csv"))
print(master.get_workers())