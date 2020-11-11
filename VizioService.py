from pyvizio import VizioAsync
import ApiService as api

async def scan_vizio(timeout=5):
    print('Scanning for vizio device(s). This could take a moment.')
    devices = VizioAsync.discovery_zeroconf(timeout)
    for d in devices:
        print('Found vizio device with host/port {}:{}'.format(d.ip, d.port))
        url = 'http://{}:{}/pairing/start'.format(d.ip, d.port);
        print('sending request to url {}'.format(url))
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36"}
        res = api.put(url, headers,
            {
                'DEVICE_NAME': 'ALOHA',
                'DEVICE_ID': '123456'
            })
        print(res)
