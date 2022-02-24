'''
Server code extracted from:

https://www.youtube.com/watch?v=M1Tm4hnvEjA

Authors:    Angel Gascon Muria      angel.gascon@estudiants.urv.cat
            Arnau Llop Iglesias     arnau.llop@estudiants.urv.cat
'''
import sys
import random
from xmlrpc.server import SimpleXMLRPCServer

class insultsAPI:

    insultList = []

    def __init__(self):
        insultFile = open("InsultList.txt", 'r')
        for line in insultFile:
            insultsAPI.insultList.append(line)     #line.strip
        insultFile.close()

    def insultme(self):
        return (insultsAPI.insultList[random.randint(0, len(insultsAPI.insultList)-1)])

    def getInsults(self):
        return insultsAPI.insultList

    def addInsult(self, newInsult):
        insultsAPI.insultList.append(newInsult)
        insultFile = open("InsultList.txt", 'a')
        insultFile.write("\n")
        insultFile.write(newInsult)
        insultFile.close()

with SimpleXMLRPCServer(("localhost", 8000), 
                        allow_none=True) as server:
    api = insultsAPI()
    server.register_function(api.insultme, "insultme")
    server.register_function(api.getInsults, "getInsults")
    server.register_function(api.addInsult, "addInsult")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nKeyboard interrupt received, exiting.")
        sys.exit(0)