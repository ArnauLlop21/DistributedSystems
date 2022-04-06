import redis
import pandas as pd

#Desde client -> r.set('read_csv', 'titanic.csv')

csvRef=False
while(True):
    #SlavePort
    r = redis.Redis(host='hostname', port=9000)
    if(csvRef):
        r.get()