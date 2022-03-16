import pandas as pd
# apply, columns, groupby, head, isin, items, max, min.
class Servant:
    #adress format "ip:port"
    def __init__(self, fileName, ip, port):
        self.df = pd.read_csv(fileName)
        self.fileName = fileName
        self.ip = ip
        self.port = port
    
    def apply(self):
        self.df.apply()
    
    def getFileName(self):
        return self.fileName

    def getIp(self):
        return self.ip

    def getPort(self):
        return self.port
    
    def head(self, n):
        return self.df.head(n)