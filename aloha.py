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
nmap = nmap3.NmapScanTechniques()

bridge_ip = ''
username = ''
scenes_dict = {}
current_scene_action = {}

#############################################################
# TODOS
# 1) create classes for hue service/vizio service that can store tokens/ip/port
# 2) cleanup
# 3) fix issue with vizio off behavior
# 4) ssl cert for vizio
# 5) ???
#############################################################

def is_connected():
    results = nmap.nmap_ping_scan(my_phone_ip)
    return results != [] and results is not None


def is_vizio_connected():
    #print(vs.get_selected_input(vizio_ip, vizio_port, vizio_token))
    return vs.is_power_on(vizio_ip, vizio_port, vizio_token)


def printd(message):
    print('{} - {}'.format(datetime.now(), message))


def load_vizio_data():
    vizio_data_path = 'vizio.txt'
    global vizio_ip
    global vizio_port
    global vizio_token
    if path.exists(vizio_data_path):
        printd('Reading locally stored vizio data')
        vizio_data_file = open(vizio_data_path)
        vizio_data =  vizio_data_file.readlines()
        vizio_ip = vizio_data[0].replace('\n', '')
        vizio_port = vizio_data[1].replace('\n', '')
        vizio_token = vizio_data[2].replace('\n', '')
    else:
        vizio_ip, vizio_port, vizio_token = vs.scan_and_get_device()
        vizio_data_file = open(vizio_data_path, 'x')
        vizio_data_file.write(str(vizio_ip))
        vizio_data_file.write('\n')
        vizio_data_file.write(str(vizio_port))
        vizio_data_file.write('\n')
        vizio_data_file.write(str(vizio_token))


def load_hue_data():
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
    else:
        raise SystemExit('Bridge not reachable - Goodbye')
    
    return bridge_ip, username


def phone_home_behavior():
    set_scene('default')


def phone_away_behavior():
    set_scene('Relax')
    
    
def vizio_on_behavior():
    # check if there is a currently selected scene - this will be important for
    # the vizio_off_behavior later one
    global current_scene_action
    current_scene_action = hs.get_current_scene(bridge_ip, username)['action']
    print('*********')
    print(current_scene_action)
    if vs.get_selected_input(vizio_ip, vizio_port, vizio_token)['ITEMS'][0]['VALUE'] == 'cast':
        set_scene('theater')
    else:
        set_scene('game')
    

def vizio_off_behavior():
    print('turning vizio off')
    print(current_scene_action)
    hs.apply_action(bridge_ip, username, current_scene_action)


def set_scene(name):
    hs.set_scene(bridge_ip, username, scenes_dict[name], True)


def main():
    global bridge_ip
    global username
    bridge_ip, username = load_hue_data()
    
    load_vizio_data()   
    # load scenes
    scenes = hs.authorized_get(bridge_ip, username, 'scenes')
    global scenes_dict
    for s in scenes:
        scenes_dict[scenes[s]['name']] = s

    routines.continuous_monitoring_multiple(routines.HueConfig(bridge_ip, username, scenes_dict),
            routines=[routines.RoutineConfig('Phone Routine', is_connected, 2,
                                             phone_home_behavior, phone_away_behavior),
                         routines.RoutineConfig('TV Routine', is_vizio_connected, 1,
                                                vizio_on_behavior, vizio_off_behavior)])


if __name__ == "__main__":
     main()