from Master import Master
from xmlrpc.server import SimpleXMLRPCServer


with SimpleXMLRPCServer(("localhost", 8000), 
                        allow_none=True) as server:
    serv = Master()
    server.register_function(serv.add, "add")
    server.register_function(serv.remove, "remove")
    server.register_function(serv.listServants, "listServants")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nKeyboard interrupt received, exiting.")
        sys.exit(0)