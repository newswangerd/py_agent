import json
import datetime
import os

from py_agent.utils import listen_for

@listen_for({'event_type': ('in', ['owm_onecall', 'brighton_busses'])})
def dashboard(event=None, handler=None):
    dashboard_file = os.environ.get('PY_AGENT_DASHBOARD_FILE')
    if not dashboard_file:
        dashboard_file = os.path.join(os.path.dirname(__file__), 'dashboard.json')
    
    current_data = {}
    try:
        with open(dashboard_file, 'r') as f:
            current_data = json.load(f)
    except:
        current_data = {}

    if event.event_type == 'owm_onecall':
        current_data['weather'] = update_weather(event)
    elif event.event_type == 'brighton_busses':
        current_data['bus_schedule'] = event.data
    
    with open(dashboard_file, 'w') as f:
        json.dump(current_data, f, indent=2)


def update_weather(event):
    data = event.data
    hourly = data['hourly']

    weather = {}
    for h in hourly:
        from_now = hours_from_now(h)
        if 0 < from_now < 9:
            weather[from_now] = analyze_conditions(h)
    
    weather['now'] = analyze_conditions(data['current'])
    return weather


def hours_from_now(hourly):
    dt = datetime.datetime.fromtimestamp(hourly['dt'])
    diff = dt - datetime.datetime.now()
    return int(diff.total_seconds() // 3600)

def analyze_conditions(data):
    profile = {
        'legs': {
            'light': (65, 1000),
            'medium': (35, 65),
            'heavy': (-200, 65)
        },
        'jacket': {
            'none': (65, 1000),
            'light': (35, 65),
            'medium': (-200, 35),
        },
        'head': {
            'none': (40, 1000), 
            'light': (-200, 40)
        },
        'gloves': {
            'none': (65, 1000),
            'light': (50, 65),
            'heavy': (-200, 50)
        },
        'shoes': {
            'light': (45, 1000),
            'heavy': (-200, 45)
        }
    }

    tempf = k_to_f(data['feels_like'])
    profile = get_temp_profile(tempf, profile)

    is_rain = False
    for w in data['weather']:
        if w['main'].lower() in ['thunderstorm', 'drizzle', 'rain']:
            is_rain = True
            break

    if is_rain:
        profile['rain_gear'] = 'light'
        profile['shoes'] = 'heavy'
    else:
        profile['rain_gear'] = 'none'
    
    return {
        'profile': profile,
        'temperature': tempf,
        'weather': data['weather'],
        'humidity': data['humidity']
    }


def get_temp_profile(temp, profile):
    prof = {}
    for item in profile:
        for weight in profile[item]:
            low, high = profile[item][weight]
            if low < temp <= high:
                prof[item] = weight
    
    return prof

def k_to_f(kelvin):
    return int(kelvin * 1.8 - 459.67)
