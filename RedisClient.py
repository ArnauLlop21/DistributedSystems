import redis
import pandas as pd

redis_host = 'localhost'
redis_port = 6379

master = redis.StrictRedis(host=redis_host, port=redis_port, decode_responses=True)
pubsubC=master.pubsub()

def client():
    petition="titanic.csv;max;Age;Client1"

    master.publish("Board" , petition)
    slaveCount=master.get("Workers")                # Get number of slaves connected to the system
    petitionTpl=tuple(map(str,petition.split(';'))) # String petition -> tuple petition. Allows for better info managing
    feedback=listenToSlaves(slaveCount,petitionTpl)
    output=treatmentResults(petitionTpl,feedback)
    for i in range(0,len(output)):
        print(output[i])


def listenToSlaves(slavesCount, petitonTpl):        # Waits for all the results of the slaves connected to the network
    pubsubC.subscribe(str(petitonTpl[3]))
    i=0
    responses=[]
    while True:
        m=pubsubC.get_message()                     # This could've been implemented with the same " for in listen" structure used in RedisSlave.py. Alternative version
        if m and m['type'] != 'subscribe' :         # We filter the subscribe messages out.
            responses.append(m['data'])
            i+=1
            if int(i) == int(slavesCount) : break   # When the number of responses recieved is equal to the number of slaves. Exit the loop
    return responses

def treatmentResults(petitionTpl, feedback):
    operation=petitionTpl[1]
    if operation == "max" or operation == "min" :   # If the petition was min or max we expect a number. As a result we can operate over that number
        df = pd.DataFrame(feedback)
        return df.max() if operation=="max" else df.min()
    else:
        return list(feedback)                       # If it wasn't min or max we expect a non manageable string, so we simply print them

if __name__ == '__main__':
    client()