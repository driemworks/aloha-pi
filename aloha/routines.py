import ipfshttpclient
import asyncio
import time
from datetime import datetime


client = ipfshttpclient.connect()


class RoutineConfig():


    def __init__(self, name, fault_tolerance, connection_status_callback,
             home_behavior, away_behavior):
        self.name = name
        self.connection_status_callback = connection_status_callback
        self.fault_tolerance = fault_tolerance,
        self.home_behavior = home_behavior
        self.away_behavior = away_behavior


def continuous_monitoring(callbacks, routines):
    print('Start monitoring')
    prev_state_array = [None] * len(routines)
    # initialize state for each routine
    for i, r in enumerate(routines, start=0):
        prev_state_array[i] = {'state': False, 'fault_count': 0}

    sleep_time = 2
    while True:
        # check statuses every 'sleep_time' ms
        time.sleep(sleep_time)
        for idx, r in enumerate(routines, start=0):
            curr_state = getattr(callbacks, r.connection_status_callback)()
            if curr_state is False:
                if prev_state_array[idx]['fault_count'] == r.fault_tolerance[0] - 1:
                    # away behavior
                    print('Goodbye ' + r.name)
                    prev_state_array[idx]['fault_count'] += 1
                    prev_state_array[idx]['state'] = curr_state
                    getattr(callbacks, r.away_behavior)()
                if prev_state_array[idx]['fault_count'] < r.fault_tolerance[0]:
                    # disconnected but awaiting fault tolerance check
                    prev_state_array[idx]['fault_count'] += 1
            else:
                prev_state_array[idx]['fault_count'] = 0
                if prev_state_array[idx]['state'] is False:
                    print('Publishing to topic  ' + r.name)
                    client.pubsub.publish(r.name, 'Home')
                    # device is_connected callback says a connection was established
                    print('Hello ' + r.name)
                    getattr(callbacks, r.home_behavior)()

                prev_state_array[idx]['state'] = curr_state
 
