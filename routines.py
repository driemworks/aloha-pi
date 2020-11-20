import asyncio
import time
import HueService as hs


class HueConfig():
    
    
    def __init__(self, bridge_ip, username, scenes):
        self.bridge_ip = bridge_ip
        self.username = username
        self.scenes = scenes
        
        
class RoutineConfig():
    

    def __init__(self, is_connected_callback, fault_tolerance,
             home_scene, home_sleep_time,
             away_scene, away_sleep_time):
        self.is_connected_callback = is_connected_callback
        self.fault_tolerance = fault_tolerance,
        self.home_scene = home_scene
        self.home_sleep_time = home_sleep_time
        self.away_scene = away_scene
        self.away_sleep_time = away_sleep_time
        


async def continuous_monitoring(bridge_ip, username,
                          is_connected_callback, fault_tolerance_threshold,
                          home_scene, home_sleep_time,
                          away_scene, away_sleep_time):
    print('Start monitoring')
    prev_state = False
    failed_pings = 0
    sleep_time = 0
    while True:
        time.sleep(sleep_time)
        curr_state = is_connected_callback()
        if curr_state is False:
            sleep_time = 5
            if failed_pings == fault_tolerance_threshold:
                # away behavior
                print('Goodbye')
                failed_pings = failed_pings + 1
                hs.set_scene(bridge_ip, username, away_scene, True)
            elif failed_pings < fault_tolerance_threshold:
                # disconnected but awaiting fault tolerance check
                failed_pings = failed_pings + 1
        else:
            failed_pings = 0
            if prev_state is False:
                print('Welcome home!')
                sleep_time = 60
                hs.set_scene(bridge_ip, username, home_scene, True)

        prev_state = curr_state
        
    

async def prepare_routines(bridge_config, routines):
    input_coroutines = []
    for r in routines:
        input_coroutines.append(continuous_monitoring(
                                    bridge_config.bridge_ip, bridge_config.username,
                                    r.is_connected_callback, r.fault_tolerance,
                                    bridge_config.scenes[r.home_scene], r.home_sleep_time,
                                    bridge_config.scenes[r.away_scene], r.away_sleep_time)
                                )
            
    #res = await asyncio.gather(*input_coroutines, return_exceptions=True)
    #return res
    return input_coroutines


def continuous_monitoring_multiple(hue_config, routines):
    print('Start monitoring')
    prev_state_array = [None] * len(routines)
    # initialize state for each routine
    for i, r in enumerate(routines, start=0):
        prev_state_array[i] = {'state': False, 'fault_count': 0}
        
    failed_pings = 0
    sleep_time = 2
    scenes = hue_config.scenes
    while True:
        # check statuses every 'sleep_time' ms
        time.sleep(sleep_time)
        for idx, r in enumerate(routines, start=0):
            curr_state = r.is_connected_callback()
            if curr_state is False:
                if prev_state_array[idx]['fault_count'] == r.fault_tolerance[0] - 1:
                    # away behavior
                    print('Goodbye')
                    prev_state_array[idx]['fault_count'] += 1
                    hs.set_scene(hue_config.bridge_ip, hue_config.username, scenes[r.away_scene], True)
                elif prev_state_array[idx]['fault_count'] < r.fault_tolerance[0]:
                    # disconnected but awaiting fault tolerance check
                    prev_state_array[idx]['fault_count'] += 1
            else:
                prev_state_array[idx]['fault_count'] = 0
                if prev_state_array[idx]['state'] is False:
                    # device is_connected callback says a connection was established
                    print('Connected')
                    hs.set_scene(hue_config.bridge_ip, hue_config.username, scenes[r.home_scene], True)

            prev_state_array[idx]['state'] = curr_state
