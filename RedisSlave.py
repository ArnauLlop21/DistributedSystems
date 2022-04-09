import redis
import pandas as pd
import RedisOpt as ro

redis_host = 'localhost'
redis_port = 6379
master = redis.StrictRedis(host=redis_host, port=redis_port, decode_responses=True)
pubsubS=master.pubsub()
def slave():
    registerNewSlave()
    subscribeToMaster()
    listenToBoard()

def registerNewSlave():
    workers=int(master.get("Workers"))      # Gets the number of currently registered slaves on the system. At least 0
    master.set("Workers", workers+1)        # Increments the number of slaves on the server to increase the information recieved by the client

def subscribeToMaster():
    pubsubS.subscribe("Board")               # Applies pubsub to the Board we want to subscribe to

def listenToBoard():                        # Method to retrieve the information from the publishing board the clients are talking them through
    i=0
    for m in pubsubS.listen():
        if m and m['type'] != 'subscribe' :
            fileTpl=tuple(map(str,m['data'].split(';')))
            result=workInPanditas(fileTpl)
            reportToSlaver(result,fileTpl[3])

def workInPanditas(fileTpl):                # Method to manage the data as the petition especified
    filePet=fileTpl[0]
    optPet=fileTpl[1]
    parmPet=fileTpl[2]
    df=pd.read_csv(filePet)
    result=calculateSlave(df,optPet,parmPet)
    return result

def calculateSlave(df,option,parameter):    # Pandas' methods
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

def reportToSlaver(info,board):                 # Method to inform our client about our results.
    master.publish(str(board),info)


if __name__ == '__main__':
    slave()
