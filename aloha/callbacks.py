import nmap3
import re

nmap = nmap3.NmapScanTechniques()

class Callbacks():
    
    def __init__(self, hueService, vizioService, nmap, scenes_dict, phone_ip):
        self.hueService = hueService
        self.vizioService = vizioService
        self.nmap = nmap
        self.scenes_dict = scenes_dict
        self.phone_ip = phone_ip

    def is_connected(self):
        results = nmap.nmap_ping_scan(self.phone_ip)
        # this is really hacky and needs to be fixed at some point
        return '(1' in results['runtime']['summary']


    def is_vizio_connected(self):
        return self.vizioService.is_power_on()

    
    def set_scene(self, name):
        self.hueService.set_scene(self.scenes_dict[name])


    def phone_home_behavior(self):
        self.set_scene('default')


    def phone_away_behavior(self):
        self.set_scene('Relax')
        
        
    def vizio_on_behavior(self):
        #print(vizioService.get_selected_input())
        if self.vizioService.get_selected_input()['ITEMS'][0]['VALUE'] == 'cast':
            self.set_scene('theater')
        else:
            self.set_scene('game')
        

    def vizio_off_behavior(self):
        self.set_scene('Relax')
