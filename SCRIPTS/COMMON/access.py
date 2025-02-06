import requests
from SCRIPTS.CRPO_COMMON.credentials import *
import json


def get_access():
    req = {"name": access_cred.get('user'), "password": access_cred.get('password')}
    header = {"content-type": "application/json"}
    response = requests.post("https://amsinwfh.hirepro.in/allow-as-dev",headers=header,
                             data=json.dumps(req, default=str), verify=False)
    get_all_resp = response.json()
    if get_all_resp['status']['yourIp']:
        print("Connected Successfully")
    else:
        print("Connection Failed")


get_access()
