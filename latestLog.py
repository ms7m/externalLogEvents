
import requests
import time
import os

global current_id
current_id = None
while True:
    time.sleep(0.5)
    req = requests.get("http://0.0.0.0:8080/logs/latest/one").json()
    if req['id'] == current_id:
        print('no event change')
        continue
    else:
        os.system('clear')
        print(req['log'])
        current_id = req['id']