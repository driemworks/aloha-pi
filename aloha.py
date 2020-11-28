import os
import yaml
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
import callbacks

scenes_dict = {}
current_scene_action = {}
vizioService = None
hueService = None


def is_connected():
    results = nmap.nmap_ping_scan(my_phone_ip)
    return results != [] and results is not None


def is_vizio_connected():
    return vizioService.is_power_on()


def phone_home_behavior():
    set_scene('default')


def phone_away_behavior():
    set_scene('Relax')
    
    
def vizio_on_behavior():
    print(vizioService.get_selected_input())
    if vizioService.get_selected_input()['ITEMS'][0]['VALUE'] == 'cast':
        set_scene('theater')
    else:
        set_scene('game')
    

def vizio_off_behavior():
    set_scene('Relax')


def set_scene(name):
    hueService.set_scene(scenes_dict[name])
    

def load_routines():
    path = 'config.yml'
    routines_out = []
    with open(path) as file:
        config_data = yaml.load(file, Loader=yaml.FullLoader)
        if config_data is not None:
            rs = config_data['routines']
            for r in rs:
                routines_out.append(
                    routines.RoutineConfig(r['name'],
                                           r['fault_tolerance'],
                                           r['status_callback'],
                                           r['status_true_callback'],
                                           r['status_false_callback']))
    return routines_out
                
        


def main():
    global hueService
    global vizioService
    hueService = hs.HueService()
    vizioService = vs.VizioService()
    # my ip address
    my_phone_ip = '192.168.1.220'
    nmap = nmap3.NmapScanTechniques()
    # load scenes
    scenes = hueService.get_scenes()
    scenes_dict = {}
    for s in scenes:
         scenes_dict[scenes[s]['name']] = s

    clback = callbacks.Callbacks(hueService, vizioService, nmap, scenes_dict, my_phone_ip)
    #routines.continuous_monitoring(routines=[
    #    routines.RoutineConfig('Phone Routine', is_connected, 2, phone_home_behavior,
    #                           phone_away_behavior),
    #    routines.RoutineConfig('TV Routine', is_vizio_connected, 1,
    #                           vizio_on_behavior, vizio_off_behavior)])
    routines.continuous_monitoring(clback, routines=load_routines())


if __name__ == "__main__":
     main()