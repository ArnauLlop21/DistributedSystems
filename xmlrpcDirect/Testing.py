from xml_rpc_Client import Client
import time
# Main
# Init client instance
client1 = Client()

try:
    while True:
        print(client1.proxies) # Prints state of workers list
        print(client1.masterP) # Prints current master
        
        print(client1.head(5, "titanic.csv"))
        time.sleep(10) # Sleep time to be able to test the master fault tolerance
        print(client1.min("PassengerId", "titanic.csv"))
        time.sleep(10) # Sleep time to be able to test the master fault tolerance                                                  
        print(client1.max("PassengerId", "titanic.csv"))
        
        print(client1.proxies) # Prints state of workers list
        print(client1.masterP) # Prints current master
        input() #Press enter to keep testing
        print("--------------\nNew test:\n--------------")
except KeyboardInterrupt:
    print('Exiting')
