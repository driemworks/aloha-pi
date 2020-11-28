from pyvizio import VizioAsync
import asyncio
import ApiService as api
from os import path


class VizioService():
    
    
    def __init__(self, data_path='vizio.txt', timeout=1):
        ip, port, auth_token = load_data(data_path, timeout)
        self.ip = ip
        self.port = port
        self.auth_token = auth_token
        
        # TODO - this is assuming there is a single vizio device
    def is_power_on(self):
        url = 'https://{}:{}/state/device/power_mode'.format(self.ip, self.port)
        headers = {"AUTH": self.auth_token}
        try:
            return api.get(url, headers=headers).json()['ITEMS'][0]['VALUE'] == 1
        except Exception as e:
            print('Oh no: {}'.format(e))
            
            
    def get_selected_input(self):
        url = 'https://{}:{}/menu_native/dynamic/tv_settings/devices/current_input'.format(self.ip, self.port)
        headers = {"AUTH": self.auth_token}
        try:
            return api.get(url, headers=headers).json()
        except Exception as e:
            print('Oh no: {}'.format(e))
            
            
    def get_current_scene(self):
        url = 'https://{}:{}/menu_native/dynamic/tv_settings/devices/current_input'.format(self.ip, self.port)
        headers = {"AUTH": self.auth_token}
        try:
            return api.get(url, headers=headers).json()
        except Exception as e:
            print('Oh no: {}'.format(e))

    
async def scan_vizio(timeout=5):
    print('Scanning for vizio device(s). This could take a moment.')
    devices = VizioAsync.discovery_zeroconf(timeout)
    return devices


def scan_and_get_device(timeout=5):
    loop = asyncio.get_event_loop()
    devices = loop.run_until_complete(scan_vizio())
    print(devices)
    d = devices[0]
    auth_token = pair(d)
    return d.ip, d.port, auth_token


# TODO - device id should not be hardcoded
def pair(d):
    base_url = 'https://{}:{}'.format(d.ip, d.port);
    url = base_url + '/pairing/start'
    headers = {"content-type": "application/json"}
    res = api.put(url, headers,
        {
            'DEVICE_NAME': 'ALOHA',
            'DEVICE_ID': '123456'
        })
    if res.status_code == 200:
        try:
            # TODO - if multiple requests for pairing made before vizio timeout
            # then request will be blocked - should handle this
            pin = input('Enter the PIN displayed on your vizio device: ')
            challenge_res_url = base_url + '/pairing/pair'
            challenge_res = api.put(challenge_res_url, headers,
                            {
                                'DEVICE_ID': '123456',
                                'CHALLENGE_TYPE': res.json()['ITEM']['CHALLENGE_TYPE'],
                                'RESPONSE_VALUE': pin,
                                'PAIRING_REQ_TOKEN': res.json()['ITEM']['PAIRING_REQ_TOKEN']
                            }
                        )
            return challenge_res.json()['ITEM']['AUTH_TOKEN']
        except Exception as e:
            print('An error occured {}', str(e))
            print('Pairing is canceled')
            # cancel pairing
            cancel_url = base_url + '/pairing/cancel'
            api.put(cancel_url, headers,
                {
                    'DEVICE_NAME': 'ALOHA',
                    'DEVICE_ID': '123456'
                })

def load_data(vizio_data_path, timeout):
    if path.exists(vizio_data_path):
        print('Reading locally stored vizio data')
        vizio_data_file = open(vizio_data_path)
        vizio_data =  vizio_data_file.readlines()
        vizio_ip = vizio_data[0].replace('\n', '')
        vizio_port = vizio_data[1].replace('\n', '')
        vizio_token = vizio_data[2].replace('\n', '')
        return vizio_ip, vizio_port, vizio_token
    else:
        vizio_ip, vizio_port, vizio_token = scan_and_get_device()
        vizio_data_file = open(vizio_data_path, 'x')
        vizio_data_file.write(str(vizio_ip))
        vizio_data_file.write('\n')
        vizio_data_file.write(str(vizio_port))
        vizio_data_file.write('\n')
        vizio_data_file.write(str(vizio_token))
        return vizio_ip, vizio_port, vizio_token
