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

# my ip address
my_phone_ip = '192.168.1.220'
# failed ping count must exceed this number before away behavior is activated
fault_tolerance = 5
nmap = nmap3.NmapScanTechniques()

def is_connected():
    results = nmap.nmap_ping_scan(my_phone_ip)
    return results != [] and results is not None


def printd(message):
    print('{} - {}'.format(datetime.now(), message))


def continuous_monitoring(fault_tolerance_threshold, bridge_ip,
                          username, home_scene, away_scene):
    printd('Start monitoring')
    prev_state = False
    failed_pings = 0
    sleep_time = 0
    while True:
        time.sleep(sleep_time)
        curr_state = is_connected()
        if curr_state is False:
            sleep_time = 5
            if failed_pings == fault_tolerance_threshold:
                # away behavior
                printd('Goodbye')
                failed_pings = failed_pings + 1
                hs.set_scene(bridge_ip, username, away_scene, True)
            elif failed_pings < fault_tolerance_threshold:
                # disconnected but awaiting fault tolerance check
                failed_pings = failed_pings + 1
                printd('ping failed: failed pings = {}'.format(failed_pings))
        else:
            failed_pings = 0
            if prev_state is False:
                printd('Welcome home!')
                sleep_time = 60
                hs.set_scene(bridge_ip, username, home_scene, True)

        prev_state = curr_state


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
            #username = '4ji63pf-CrZFhlA1ewzj4uEMMqxuzh-mFT0ZwUFM'
            uname_file = open(uname_path, 'x')
            uname_file.write(username)
        #groups = hs.authorized_get(bridge_ip, username, 'groups')
        # i only have group = 1
        #for g in groups:
        #    print(g + ': ' + groups[g]['name'])
        scenes = hs.authorized_get(bridge_ip, username, 'scenes')
        scenes_dict = {}
        for s in scenes:
            scenes_dict[scenes[s]['name']] = s
            #print(s + ': ' +  scenes[s]['name'])
        continuous_monitoring(fault_tolerance, bridge_ip, username, scenes_dict['default'], scenes_dict['Relax'])
    else:
        raise SystemExit('Bridge not reachable - Goodbye') 


if __name__ == "__main__":
    #vs.discover_vizio()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(vs.scan_vizio())
    loop.close()
    #main()