import json
import requests
import datetime

from config import SPARK_PPL, SPARK_ROOMS, MY_TOKEN, SPARK_MSG


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

    room_dict = json.loads(resp.text)

    return room_dict['id']

def writeMessage(auth_token, room_id, text):
    url = SPARK_MSG
    headers = {'Authorization': 'Bearer ' + auth_token}

    payload = {'roomId' : room_id,  'text' : text }

    resp =  resp = requests.post(url,json=payload, headers=headers)