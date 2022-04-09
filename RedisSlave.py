import redis

redis_host = 'localhost'
redis_port = 6379

master = redis.StrictRedis(host=redis_host, port=redis_port, decode_responses=True)

def slave():
    registerNewSlave()
    subscribeToMaster()
#    listenToBoard()

def registerNewSlave():
    workers=int(master.get("Workers"))      # Gets the number of currently registered slaves on the system. At least 0
    master.set("Workers", workers+1)        # Increments the number of slaves on the server to increase the information recieved by the client

def subscribeToMaster():
    pubsub = master.pubsub()                # Generates the instance pubsub tied to the master server
    pubsub.subscribe("Board")               # Applies pubsub to the Board we want to subscribe to

#def listenToBoard():


if __name__ == '__main__':
    master.set("Workers", 0)
    slave()
#    slave()
#    slave()