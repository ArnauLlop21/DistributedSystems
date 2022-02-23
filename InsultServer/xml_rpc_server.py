'''
Server code extracted from:

https://www.youtube.com/watch?v=M1Tm4hnvEjA

Authors:    Angel Gascon Muria      angel.gascon@estudiants.urv.cat
            Arnau Llop Iglesias     arnau.llop@estudiants.urv.cat
'''

import random
from xmlrpc.server import SimpleXMLRPCServer

insultFile = open("InsultList.txt", 'r')
insultList = []

for line in insultFile:
    insultList.append(line)     #Si no xusca bé provem line.strip

insultFile.close()

def insultme():
    return insultList[random.randint(0, len(insultList)-1)]

def getInsults():
    return insultList

def addInsult(newInsult):
    insultList.append(newInsult)
    insultFile = open("InsultList.txt", 'a')
    insultFile.write("\n")
    insultFile.write(newInsult)
    insultFile.close()

server = SimpleXMLRPCServer(("localhost",8000))
server.register_function(insultme, "insultme")
server.register_function(getInsults, "getInsults")
server.register_function(addInsult, "addInsult")

server.serve_forever()


