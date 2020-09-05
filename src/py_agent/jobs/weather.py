import requests
import json
import hashlib

from py_agent.credentials import get_credential

def weather(handler=None):
    lat = '42.358429'
    lon = '-71.059769'
    token = get_credential('open_weather_map')

    r = requests.get(
         'https://api.openweathermap.org/data/2.5/onecall?'
        f'lat={lat}&'
        f'lon={lon}&'
        f'appid={token}')

    m = hashlib.sha1()
    m.update(r.text.encode('utf-8'))
    
    handler.publish('owm_onecall', m.hexdigest(), r.json())