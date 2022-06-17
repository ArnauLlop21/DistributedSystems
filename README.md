# Distribuited Systems
## Task1: Direct and indirect communication in XMLRPC, gRPC, Redis and RabbitMQ
In this task 4 models of direct and indirect communication have been implemented.
This project tries to simulate Dask performance with a cluster of Pandas Workers.
For the sake of the testing we have used the titanic.csv but it can be used with any CSV.

https://github.com/datasciencedojo/datasets/blob/master/titanic.csv

### Direct
XMLRPC: Works with no IDL and because of that is very slow.
gRPC: Uses proto IDL and makes communication much more efficient.
### Indirect (Servers implemented on a Docker)
Redis: Uses a DataBase-alike model. We've implemented it in a pubsub communication scheme.
RabbitMQ: It has been implemented in a pubsub communication scheme using fanout exchanges.

The developpement of RabbitMQ has been guided by the following youtube videos:

https://www.youtube.com/watch?v=iQ4kENLfaNI&list=PLalrWAGybpB-UHbRDhFsBgXJM1g6T4IvO

## Task2: Consistency and Fault Tolerance
This has been implemented in the XMLRPC program but with the correct modifications the concepts can be used in every architecture.
### Important note
This implementation has been simplified by considering every one of the servers running are doing so in localhost. With very simple modifications it can be used with IPs or URLs. But this is not the case in our prototype.
This means that the identity of the machine is ultimately determined by the port being used. This is not a realistic approach but can be useful in academic environments.
### How to use it?
To initialize the Distributed System we must execute:
Initialize Redis (Docker, we are using port 6379 at localhost)
Initialize master, where 1 indicates that we are creating the master (the first master creation is at port 8000 by default)

`python xml_rpc_MW.py 1`

Initialize workers, where 0 indicates that we are creating a worker and 900x sets worker port
``` bash
python xml_rpc_MW.py 0 9001 #First server. 0 means worker. 9001 is the port
python xml_rpc_MW.py 0 9002
python xml_rpc_MW.py 0 9003
#etc
```
Run Testing.py or any .py that's able to instance our client and run it

`python Testing.py`

During the execution if master fails, one of the workers will take its place.
During the execution if a worker fails, the system will keep working.
During the execution if we create another worker, it will be added to the DS.

### Redis instance
The following code instances a Redis server. It is important to make sure the port and the host matches your use case as well. Otherwise, change it appropriately
``` python
redis_host = 'localhost'
redis_port = 6379
r = redis.StrictRedis(host=redis_host, port=redis_port, decode_responses=True)
```

### Master substitution. Reelection method
With the following lines of code we are able to implement the Bully algorithm.
The **Bully algorithm** makes sure the substitute of the master, whenever it fails, is the best fit for the job. This, in our prototype, is managed with a pseudorandom integer that does not make much sense. In a real approach this can be used with a real performance indicator such as low latency or the capacity of the machine to answer petitions.
```python
def turn_into_master(node):
    global im_master, master_port, change
    im_master = True
    change = True
    master_port = server.server_address[1] 
    r.set("master" , master_port)
    remove_node(node)

def should_we_bully_you():
    global bullId
    return bullId

def lets_decide_who_to_bully():
    global workers_list
    minimumBull = [sys.maxsize, 0]
    for worker in workers_list:
        try:
            proxy = [ServerProxy(worker, allow_none=True).should_we_bully_you() , worker]
            if proxy[0] < minimumBull[0]: 
                minimumBull = proxy
        except socketError:
            print("Something has gone kaboom xd")
    return minimumBull[1]

```


# Authors
The authors of this project are:
- https://github.com/AngelGascon
- https://github.com/ArnauLlop21

This is the result of an academic project made in URV for the Distribuited Systems course.
