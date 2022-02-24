'''
Client code extracted from:

https://www.youtube.com/watch?v=M1Tm4hnvEjA

Authors:    Angel Gascon Muria      angel.gascon@estudiants.urv.cat
            Arnau Llop Iglesias     arnau.llop@estudiants.urv.cat
'''

import xmlrpc.client
import os

def clearConsole():
    command = 'clear'
    if os.name in ('nt', 'dos'):  # If Machine is running on Windows, use cls
        command = 'cls'
    os.system(command)

proxy =  xmlrpc.client.ServerProxy("http://localhost:8000")

option = 0
while(option != 4):
    print("1: InsultMe\n2: Get all insults\n3: Add a new insult\n4: Exit\n")
    option=int(input("Select what you would like to do..."))
    print("\n")
    if(option==1):
        print(proxy.insultme())
    elif(option==2):
        print(proxy.getInsults())
    elif(option==3):
        newInsult = input("What insult do you want to add? ")
        proxy.addInsult(newInsult)
    input("Press enter to continue...")
    clearConsole()

print("Program ended.")