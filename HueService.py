import requests


def discover_bridge():
    res = requests.get('https://discovery.meethue.com/')
    return res.json()[0]['internalipaddress']


def is_active(ip):
    try:
        requests.get('http://' + ip)
        return True
    except Exception as e:
        return False
    

def connect_to_bridge(ip):
    url = 'http://' + ip + '/api'
    body = {'devicetype': 'aloha#raspberry-pi'}
    res = requests.post(url, json=body)
    res_json = res.json()[0]
    if 'error' in res_json:
        print('Press the link button on your bridge to pair with the device')
        try:
            input('Press enter to continue')
            return connect_to_bridge(ip)
        except SyntaxError:
            raise SystemExit('Goodbye')
    elif 'success' in res_json:
        return res_json['success']['username']
    

def build_url(ip, username, resource):
    return 'http://' + ip + '/api/' + username + '/' + resource
    

def authorized_get(ip, username, resource):
    res = requests.get(build_url(ip, username, resource))
    return res.json()
    

def authorized_put(ip, username, resource, body):
    url = build_url(ip, username, resource)
    try:
        res = requests.put(url, json=body)
        return res.json()
    except Exception as e:
        raise SystemExit('uhoh')
    


def set_scene(bridge_ip, username, scene_id, state):
    return authorized_put(bridge_ip, username, 'groups/1/action', {
        'on': state,
        'scene': scene_id
    })