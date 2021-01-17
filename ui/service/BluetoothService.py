import dbus

bus = dbus.SystemBus()
proxy_object = bus.get_object('org.bluez', "/")
manager = dbus.Interface(proxy_object, "org.freedesktop.DBus.ObjectManager")

dev_1 = 'org.bluez.Device1'

def list_connected_devices():
    connected_devices = []
    managed_objects = manager.GetManagedObjects()
    for path in managed_objects:
        is_connected = managed_objects[path].get(dev_1, {}).get('Connected', False)
        if is_connected:
            connected_device = managed_objects[path].get(dev_1, {})
            connected_devices.append(connected_device)
            addr = connected_device.get('Address')
            name = connected_device.get('Name')
            print(f'Device {name} [{addr}] is connected')

    return connected_devices


# if __name__ == '__main__':
#     list_connected_devices()
