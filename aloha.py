import os
import os.path
from os import path
import time
from datetime import datetime
import nmap3
import asyncio
import HueService as hs
import VizioService as vs
from pyvizio import VizioAsync
import ApiService as api
import routines

# my ip address
my_phone_ip = '192.168.1.220'
vizio_ip = ''
vizio_port = ''
vizio_token = ''
# failed ping count must exceed this number before away behavior is activated
fault_tolerance = 5
nmap = nmap3.NmapScanTechniques()

def is_connected():
    results = nmap.nmap_ping_scan(my_phone_ip)
    return results != [] and results is not None


def is_vizio_connected():
    return vs.is_power_on(vizio_ip, vizio_port, vizio_token)


def printd(message):
    print('{} - {}'.format(datetime.now(), message))


def main():
    bridge_ip = hs.discover_bridge()
    printd('Discovered hue bridge at {}'.format(bridge_ip))
    # check if bridge is reachable
    is_active = hs.is_active(bridge_ip)
    if is_active:
        printd('Bridge is reachable')
        uname_path = 'username.txt';
        # check to see if username already exists
        if path.exists(uname_path):
            printd('Reading locally stored username')
            uname_file = open(uname_path)
            username = uname_file.read()
        else:
            printd('Username not found - authorize with the bridge')
            username = hs.connect_to_bridge(bridge_ip)
            uname_file = open(uname_path, 'x')
            uname_file.write(username)
            
        # load scenes
        scenes = hs.authorized_get(bridge_ip, username, 'scenes')
        scenes_dict = {}
        for s in scenes:
            scenes_dict[scenes[s]['name']] = s
        # store/read from disk
        # TODO - move this to its own function
        loop = asyncio.get_event_loop()
        devices = loop.run_until_complete(vs.scan_vizio())
        d = devices[0]
        global vizio_ip
        vizio_ip = d.ip
        global vizio_port
        vizio_port = d.port
        global vizio_token
        vizio_token = vs.pair(devices[0])

        routines.continuous_monitoring_multiple(routines.HueConfig(bridge_ip, username, scenes_dict),
                             routines=[routines.RoutineConfig(is_connected, 5,
                                                              'default', 60,
                                                              'Relax', 5),
                             routines.RoutineConfig(is_vizio_connected, 1,
                                                  'spicy', 2,
                                                  'Relax', 2)])
    else:
        raise SystemExit('Bridge not reachable - Goodbye') 


if __name__ == "__main__":
    main()