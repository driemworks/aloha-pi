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



def continuous_monitoring_test(ip, port, token, fault_tolerance_threshold, bridge_ip, username, home_scene, away_scene):
    printd('Start monitoring')
    prev_state = False
    faults = 0
    sleep_time = 0
    while True:
        time.sleep(sleep_time)
        curr_state = vs.is_power_on(ip, port, token)
        if curr_state is False:
            sleep_time = 1
            if faults == fault_tolerance_threshold:
                # away behavior
                printd('Goodbye')
                faults = faults + 1
                hs.set_scene(bridge_ip, username, away_scene, True)
            elif faults < fault_tolerance_threshold:
                # disconnected but awaiting fault tolerance check
                faults = faults + 1
                #printd('ping failed: failed pings = {}'.format(failed_pings))
        else:
            faults = 0
            if prev_state is False:
                printd('Welcome home!')
                sleep_time = 2
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
            uname_file = open(uname_path, 'x')
            uname_file.write(username)
            
        # load scenes
        scenes = hs.authorized_get(bridge_ip, username, 'scenes')
        scenes_dict = {}
        for s in scenes:
            scenes_dict[scenes[s]['name']] = s
        
        # TODO - CAVEAT: the raspberry pi only has four cores
        # option 1: run separate threads for each device/event/api we want to monitor
        # option 2: monitor based on timer events
        
        #continuous_monitoring(fault_tolerance, bridge_ip, username, scenes_dict['default'], scenes_dict['Relax'])
        # TODO - store auth token same way as username
        loop = asyncio.get_event_loop()
        devices = loop.run_until_complete(vs.scan_vizio())
        loop.close()
        d = devices[0]
        ip = d.ip
        port = d.port
        vizio_auth_token = vs.pair(devices[0])
        continuous_monitoring_test(ip, port, vizio_auth_token, 1, bridge_ip, username, scenes_dict['spicy'], scenes_dict['default'])
    else:
        raise SystemExit('Bridge not reachable - Goodbye') 


if __name__ == "__main__":
    #vs.discover_vizio()
    #loop = asyncio.get_event_loop()
    #devices = loop.run_until_complete(vs.scan_vizio())
    #loop.close()
    #d = devices[0]
    #ip = d.ip
    #port = d.port
    #vizio_auth_token = vs.pair(devices[0])
    #continuous_monitoring_test(ip, port, vizio_auth_token, 3, )
    main()