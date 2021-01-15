import requests
from os import path

class HueService():
    
    def __init__(self, data_path='../hue_config.txt'):
        ip, username = load_data(data_path)
        #scenes = authorized_get('scenes')
        #scenes_dict = {}
        #for s in scenes:
        #    scenes_dict[scenes[s]['name']] = s
        self.ip = ip
        self.username = username


    def apply_action(self, action):
        try:
            authorized_put(self, 'groups/1/action', action)
        except Exception as e:
            print('could not apply action: {}'.format(e))

    
    def get_scenes(self):
        url = 'http://{}/api/{}/scenes'.format(self.ip, self.username)
        try:
            res = requests.get(url)
            return res.json()
        except Exception as e:
            print('Could not get resource {}'.format(e))


    def set_scene(self, scene_id):
        url = 'http://{}/api/{}/groups/1/action'.format(self.ip, self.username)
        try:
            res = requests.put(url, json={
            'on': True,
            'scene': scene_id
        })
            return res.json()
        except Exception as e:
            raise SystemExit('HTTP PUT failed with reason: {}'.format(e))


    def get_current_state(self):
        try:
            return authorized_get(self, 'groups/1')
        except Exception as e:
            print('Could not get current scene: {}'.format(e))
            return 'default'
        
    def authorized_get(self, resource):
        url = 'http://{}/api/{}/{}'.format(self.ip, self.username, resource)
        try:
            res = requests.get(url)
            print(res)
            return res.json()
        except Exception as e:
            print('Could not get resource {}'.format(resource))
        

    def authorized_put(self, resource, body):
        url = 'http://{}/api/{}/{}'.format(self.ip, self.username, resource)
        try:
            res = requests.put(url, json=body)
            return res.json()
        except Exception as e:
            raise SystemExit('HTTP PUT failed with reason: {}'.format(e))


def discover_bridge():
    res = requests.get('https://discovery.meethue.com/')
    return res.json()[0]['internalipaddress']


        
    def build_url(self, resource):
        return 'http://{}/api/{}/{}'.format(self.ip, self.username, resource)


def is_active(ip):
    try:
        requests.get('http://' + ip)
        return True
    except Exception as e:
        return False
    
    
    def build_url(self, resource):
        return 'http://' + self.ip + '/api/' + self.username + '/' + resource
    

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
    
    
def load_data(uname_path):
    ip = discover_bridge()
    print('Discovered hue bridge at {}'.format(ip))
    # check if bridge is reachable
    if is_active(ip):
        print('Bridge is reachable')
        # check to see if username already exists
        if path.exists(uname_path):
            print('Reading locally stored username')
            uname_file = open(uname_path)
            username = uname_file.read()
        else:
            print('Username not already stored - authorize with the bridge')
            username = connect_to_bridge(ip)
            uname_file = open(uname_path, 'x')
            uname_file.write(username)
    else:
        raise SystemExit('Bridge not reachable - Goodbye')
    
    return ip, username