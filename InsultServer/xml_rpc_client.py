'''
Client code extracted from:

https://www.youtube.com/watch?v=M1Tm4hnvEjA

Authors:    Angel Gascon Muria      angel.gascon@estudiants.urv.cat
            Arnau Llop Iglesias     arnau.llop@estudiants.urv.cat
'''

import xmlrpc.client

proxy = xmlrpc.client.ServerProxy("http://localhost:8000")

option = 0
while(option != 4):
    print("1: InsultMe\n2: Get all insults\n3: Add a new insult\n4: Exit")
    option=int(input("Select what you would like to do..."))
    if(option==1): print(proxy.insultme())
    elif(option==2): print(proxy.getInsults())
    elif(option==3): proxy.addInsult(input("What insult do you want to add? "))
