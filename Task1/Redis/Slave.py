import redis

redis_host = 'localhost'
redis_port = 6379

master = redis.StrictRedis(host=redis_host, port=redis_port, decode_responses=True)

def slave(name):
    addSlave(name)
    print("Number of workers: " + str(master.get("Workers")))
    print("\nThe list of workers is:\n")
    for i in master.get("Workers"):
        print(str(master.lindex("LlistaWorkers", i))+"\n")
    while True:
        
        break

def addSlave(name):
    master.rpush("LlistaWorkers", name)
    workers = master.get("Workers")
    if workers == "None":
        numWorkers = 0
    else:
        numWorkers = int(workers)
        
    # Longitud de la llista, canviar.
    master.set("Workers", numWorkers+1)


if __name__ == '__main__':
    slave("Slave0")