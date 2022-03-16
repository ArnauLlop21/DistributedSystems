from numpy import void
from Master import Master
from Servant import Servant

class Client:

    def __init__(self, refMaster):
        self.refMaster = refMaster