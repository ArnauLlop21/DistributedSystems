import redis

redis_host = 'localhost'
redis_port = 6379

master = redis.StrictRedis(host=redis_host, port=redis_port, decode_responses=True)

if __name__ == '__main__':
    #To be implemented yet
    exit        # INSTRUCTION TO BE DELETED!!! Only to avoid warnings due to unimplemented code