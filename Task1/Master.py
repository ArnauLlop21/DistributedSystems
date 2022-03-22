# Li demana al servant 
from Servant import Servant


class Master:

    def __init__(self):
        self.listedServants = []

    def add(self, newServant):
        self.listedServants.append(newServant)

    def remove(self, oldServant):
        self.listedServants.remove(oldServant)
    
    def listServants(self):
        aux = []
        for serve in self.listedServants:
            aux.append(serve)
        return aux