import dbus

bus = dbus.SystemBus()
proxy_object = bus.get_object('org.bluez', "/")
manager = dbus.Interface(proxy_object, "org.freedesktop.DBus.ObjectManager")

dev_1 = 'org.bluez.Device1'

def list_connected_devices():
    connected_devices = []
    managed_objects = manager.GetManagedObjects()
    for path in managed_objects:
        device = managed_objects[path].get(dev_1, {})
        is_connected = device.get('Connected', False)
        if is_connected:
            connected_devices.append(device)
            addr = device.get('Address')
            name = device.get('Name')
            print(f'Device {name} [{addr}] is connected')

    return connected_devices


# if __name__ == '__main__':
#     list_connected_devices()
