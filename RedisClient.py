import redis

redis_host = 'localhost'
redis_port = 6379

master = redis.StrictRedis(host=redis_host, port=redis_port, decode_responses=True)

def client():
    master.publish("Board" , "titanic.csv;isin;[59,18]")
#    master.publish("Board" , 'titanic.csv;groupby;["PassengerId"]')
#    master.publish("Board" , "titanic.csv,apply")
    

if __name__ == '__main__':
    client()