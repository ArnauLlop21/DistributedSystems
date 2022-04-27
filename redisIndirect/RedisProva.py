import redis
import json
import time

redis_host = 'localhost'
redis_port = 6379

def redis_string():
    try:
        name = "hola"
        r = redis.StrictRedis(host=redis_host, port=redis_port, decode_responses=True)
        r.mset({"Angel": "Guapo", "Arnau": "Desquiciat"})

        r.set(name, "LlistaGuai")
        print(r.get(name))
        
    except:
        print("AH")

def redis_number():
    try:
        r = redis.StrictRedis(host=redis_host, port=redis_port, decode_responses=True)
        r.set("number", "1023")
        msg = r.get("number")
        print(msg)
    except:
        print("AH2")

def provaOutputPipe():
    try:
        redis_client = redis.Redis(host=redis_host,
        port=redis_port, decode_responses=True)
        pipe = redis_client.pipeline()
        data_list = [{"key":"1"},
                    {"key":"2"},
                    {"key":"3"},
                    {"key":"4"},
                    {"key":"5"},
                    {"key":"6"},
                    {"key":"7"}]
        for item in data_list:
            pipe.get(item['key'])
        get_response = pipe.execute()
        print("bulk get response : ", get_response)
    except:
        print("AH3")

def provaInputPipe():
    try:
        redis_client = redis.Redis(host='localhost',
        port=6379, db=0, ssl=False)
        pipe = redis_client.pipeline()

        data_list = [{"key":"1", "value":"apple"},
             {"key":"2", "value":"mango"},
             {"key":"3", "value":"grapes"},
             {"key":"4", "value":"orange"},
             {"key":"5", "value":"pineapple"},
             {"key":"6", "value":"guava"},
             {"key":"7", "value":"watermelon"}]

        for item in data_list:
            pipe.set(item['key'], json.dumps({item['key'] : item['value']}))
        set_response = pipe.execute()
        print("bulk insert response : ", set_response)
    except:
        print("AH4")

def provaPubSub():
    try:
        redis_client = redis.Redis(host='localhost',port=6379, decode_responses=True)
        pubsub = redis_client.pubsub()
        pubsub.subscribe('Taulell1')
        time.sleep(1)
        prova = {"titanic.csv","min"}
        #redis_client.publish('Taulell1', "HOLA")
        #redis_client.publish('Taulell1', "Valor2")
        redis_client.publish('Taulell1', "PubSubhaha")
        print(pubsub.get_message())
        print(pubsub.get_message())

    except:
        print("AHPubsub")

def provaTupla():
    string="a;b;c;d;e"
    strTupl=tuple(map(str,string.split(';')))
    #a=strTupl.get(0)            # Not okay
    a=strTupl[0]
    b=strTupl[1]
    c=strTupl[2]
    d=strTupl[3]
    e=strTupl[4]
    print(a,b,c,d,e)      # Unpacking should go n to n.
    a=a+"()"
    print (a)
    printProva="print(a)"
    eval(printProva)
    a="a"
    b=["a","b"]
    print(len(a))
    print(len(b))
    print(a[0])
    redis_client = redis.Redis(host='localhost',port=6379, decode_responses=True)
    print(redis_client.get("Workers"))


if __name__ == '__main__':
    #redis_string()
    #redis_number()
    #provaInputPipe()
    #provaOutputPipe()
    #provaPubSub()
    provaTupla()