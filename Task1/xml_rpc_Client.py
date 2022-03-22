from xmlrpc.client import ServerProxy
import pandas as pd

master = ServerProxy('http://localhost:8000', allow_none=True)

workers_list = master.get_workers()

for worker in workers_list:
    wk = ServerProxy(worker, allow_none=True)
    wk.read_csv("titanic.csv")
    print(wk.head(5))