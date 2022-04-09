import redis
import time
import pandas as pd
import RedisOpt as ro

redis_host = 'localhost'
redis_port = 6379
master = redis.StrictRedis(host=redis_host, port=redis_port, decode_responses=True)
pubsub=master.pubsub()
def slave():
    registerNewSlave()
    subscribeToMaster()
    listenToBoard()

def registerNewSlave():
    workers=int(master.get("Workers"))      # Gets the number of currently registered slaves on the system. At least 0
    master.set("Workers", workers+1)        # Increments the number of slaves on the server to increase the information recieved by the client

def subscribeToMaster():
    pubsub.subscribe("Board")               # Applies pubsub to the Board we want to subscribe to

""" def listenToBoard():
    while True:
        message=pubsub.get_message()
        time.sleep(2)
        if message and message['type'] != 'subscribe':
            print(message) """
def listenToBoard():
    i=0
    for m in pubsub.listen():
        if m and m['type'] != 'subscribe' :
            petition=m['data']
            #print(petition)
            workInPanditas(petition)

def workInPanditas(petition):
    fileTpl=tuple(map(str,petition.split(';')))
    filePet,optPet,parmPet=fileTpl
    print(filePet)
    print(optPet)
    print(parmPet)
    df=pd.read_csv(filePet)
    result=calculateSlave(df,optPet,parmPet)
    print(result)

def calculateSlave(df,option,parameter):
    if parameter == "null" :
        print("parameter null")
        if option == "columns":
            return ro.columns(df)
        elif option == "items":
            return ro.items(df)
        else: return "Something went wrong"
    else:
        print("parameter not null")
        if option == "apply":
            return ro.apply(df,parameter)
        elif option == "groupby":
            return ro.groupby(df,parameter)
        elif option == "head":
            return ro.head(df, int(parameter))
        elif option == "isin":
            return ro.isin(df,parameter)
        elif option == "max":
            return ro.max(df,parameter)
        elif option == "min":
            return ro.min(df,parameter)
        else: return "Something went wrong"

if __name__ == '__main__':
    master.set("Workers", 0)
    slave()
#    slave()
#    slave()