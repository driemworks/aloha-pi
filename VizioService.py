from pyvizio import VizioAsync
import ApiService as api


async def scan_vizio(timeout=5):
    print('Scanning for vizio device(s). This could take a moment.')
    devices = VizioAsync.discovery_zeroconf(timeout)
    return devices


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


# TODO - this is assuming there is a single vizio device
def is_power_on(ip, port, auth_token):
    url = 'https://{}:{}/state/device/power_mode'.format(ip, port)
    headers = {"AUTH": auth_token}
    try:
        return api.get(url, headers=headers).json()['ITEMS'][0]['VALUE'] == 1
    except Exception as e:
        print('AWW SHIT: {}'.format(e))