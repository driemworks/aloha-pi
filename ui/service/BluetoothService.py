import pydbus

bus = pydbus.SystemBus()
adapter = bus.get('org.bluez', '/org/bluez/hci0')
manager = bus.get( 'org.bluez', '/')


dev_1 = 'org.bluez.Device1'


def list_connected_devices():
    managed_objects = manager.GetManagedObjects()
    for path in managed_objects:
        is_connected = managed_objects[path].get(dev_1, {}).get('Connected', False)
        if is_connected:
            connected_device = managed_objects[path].get(dev_1, {})
            addr = connected_device.get('Address')
            name = connected_device.get('Name')
            print(f'Device {name} [{addr}] is connected')


if __name__ == '__main__':
    list_connected_devices()