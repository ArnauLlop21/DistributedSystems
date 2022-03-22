from numpy import void
from Master import Master
from Servant import Servant

class Client:

    def __init__(self, refMaster):
        self.refMaster = refMaster
    
    def setAddr(self, addr):
        self.addr = addr
    
    def getAddr(self):
        return self.addr