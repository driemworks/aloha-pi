import asyncio
import time
import HueService as hs


class HueConfig():
    
    
    def __init__(self, bridge_ip, username, scenes):
        self.bridge_ip = bridge_ip
        self.username = username
        self.scenes = scenes
        
        
class RoutineConfig():
    

    def __init__(self, name, connection_status_callback, fault_tolerance,
             home_behavior, away_behavior):
        self.name = name
        self.connection_status_callback = connection_status_callback
        self.fault_tolerance = fault_tolerance,
        self.home_behavior = home_behavior
        self.away_behavior = away_behavior


def continuous_monitoring_multiple(hue_config, routines):
    print('Start monitoring')
    prev_state_array = [None] * len(routines)
    # initialize state for each routine
    for i, r in enumerate(routines, start=0):
        prev_state_array[i] = {'state': False, 'fault_count': 0}

    sleep_time = 2
    scenes = hue_config.scenes
    while True:
        # check statuses every 'sleep_time' ms
        time.sleep(sleep_time)
        for idx, r in enumerate(routines, start=0):
            curr_state = r.connection_status_callback()
            if curr_state is False:
                if prev_state_array[idx]['fault_count'] == r.fault_tolerance[0] - 1:
                    # away behavior
                    print('Goodbye ' + r.name)
                    prev_state_array[idx]['fault_count'] += 1
                    prev_state_array[idx]['state'] = curr_state
                    #hs.set_scene(hue_config.bridge_ip, hue_config.username, scenes[r.away_scene], True)
                    r.away_behavior()
                if prev_state_array[idx]['fault_count'] < r.fault_tolerance[0]:
                    # disconnected but awaiting fault tolerance check
                    prev_state_array[idx]['fault_count'] += 1
            else:
                prev_state_array[idx]['fault_count'] = 0
                if prev_state_array[idx]['state'] is False:
                    # device is_connected callback says a connection was established
                    print('Hello ' + r.name)
                    r.home_behavior()
                    #hs.set_scene(hue_config.bridge_ip, hue_config.username, scenes[r.home_scene], True)

                prev_state_array[idx]['state'] = curr_state
 