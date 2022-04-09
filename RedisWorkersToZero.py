import redis


redis_host = 'localhost'
redis_port = 6379
master = redis.StrictRedis(host=redis_host, port=redis_port, decode_responses=True)
master.set("Workers",0)