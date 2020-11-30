import os
import yaml
from os import path
import nmap3
import HueService as hs
import VizioService as vs
import routines
import callbacks

scenes_dict = {}
current_scene_action = {}
vizioService = None
hueService = None
    
def load_yaml(path):
    path = 'config.yml'
    routines_out = []
    with open(path) as file:
        return yaml.load(file, Loader=yaml.FullLoader)


def load_routines(config_data):
    routines_out = []
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
    config_data = load_yaml('config.yml')
    print(config_data)
    # my ip address
    device_ip = config_data['device'][0]['ip']
    nmap = nmap3.NmapScanTechniques()
    # load scenes
    scenes = hueService.get_scenes()
    scenes_dict = {}
    for s in scenes:
         scenes_dict[scenes[s]['name']] = s

    clback = callbacks.Callbacks(hueService, vizioService, nmap, scenes_dict, device_ip)
    routines.continuous_monitoring(clback, routines=load_routines(config_data))



if __name__ == "__main__":
    main()
