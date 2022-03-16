from Servant import Servant
from xmlrpc.server import SimpleXMLRPCServer
import sys

with SimpleXMLRPCServer(("localhost", 8000), 
                        allow_none=True) as server:
    serv = Servant()
    server.register_function(serv.apply, "apply")
    server.register_function(serv.getFileName, "getFileName")
    server.register_function(serv.head, "head")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nKeyboard interrupt received, exiting.")
        sys.exit(0)