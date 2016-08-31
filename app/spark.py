import json
import requests

from config import SPARK_PPL, MY_TOKEN


def get_me_name(auth_token=MY_TOKEN):
    url = SPARK_PPL + "/me"
    headers = {'Authorization': 'Bearer ' + auth_token}

    resp = requests.get(url, headers=headers)

    me_name = json.loads(resp.text)

    return me_name['displayName']
