import json
import requests
import datetime

from config import SPARK_PPL, SPARK_ROOMS, MY_TOKEN


def get_me_name(auth_token=MY_TOKEN):
    url = SPARK_PPL + "/me"
    headers = {'Authorization': 'Bearer ' + auth_token}

    resp = requests.get(url, headers=headers)

    me_name = json.loads(resp.text)

    return me_name['displayName']

def createRoom(auth_token=MY_TOKEN):
    url = SPARK_ROOMS
    headers = {'Authorization': 'Bearer ' + auth_token}

    now = datetime.datetime.now()
    room_name = 'ACI+SPARK - ' + now.isoformat()

    payload = {'title' : room_name}

    resp = requests.post(url,json=payload, headers=headers)

    return str(resp.status_code)
