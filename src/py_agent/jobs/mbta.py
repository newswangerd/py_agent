import requests
import json
import hashlib

# stops near given lat and lon
# https://api-v3.mbta.com/stops?filter[latitude]=42.349338&filter[longitude]=-71.153612&filter[radius]=0.001
# stops
#   - 1035: 86 to cambridge
#   - 973: 501 to downtown
#   - 1084: 57 to kenmore
# endpoint for full schedule and prediction of next arrival
# https://api-v3.mbta.com/schedules?filter[stop]=1035&include=prediction&sort=-arrival_time

def mbta_busses(handler=None):
    stops = {
        '86_to_cambridge': {'stop': 1035, 'route': 86},
        '501_to_downtown': {'stop': 973, 'route': 501},
        '57_to_kenmore': {'stop': 918, 'route': 57}
    }
    
    results = {}

    for stop in stops:
        id = stops[stop]

        r = requests.get(
            'https://api-v3.mbta.com/predictions?filter[stop]={}&filter[route]={}&sort=arrival_time'.format(
                id['stop'], id['route']))

        data = r.json()['data']
        results[stop] = []
        for p in data:
            if(p['attributes']['arrival_time']):
              results[stop].append(p['attributes']['arrival_time'])
    
    data_str = json.dumps(results).encode('utf-8')
    sha = hashlib.sha1()
    sha.update(data_str)

    handler.publish('brighton_busses', sha.hexdigest(), results)