# ALOHA
Aloha is a simple IoT application to allow automation of Philips Hue lights based on external sources. This is definitely a work in progress, and the future state is not well defined, but the general idea is to build a raspberry-pi based IoT Hub that is capable of easily integrating with new input sources and configuring output behavior.

 Current capabilities include:
- home/away behavior based on devices currently connected to the network, 
- Philips Hue state automated based on Vizio device status (power on, power off, input selection)


## Getting Started
### Setup
- install nmap
- TODO

## TODOS
- [-] raspberry-pi configuration script
    - bluetooth config:
       - pi@raspberrypi:~/work/aloha $ sudo mkdir /etc/systemd/system/bluetooth.service.d/
pi@raspberrypi:~/work/aloha $ sudo touch /etc/systemd/system/bluetooth.service.d/01-disable-sap-plugin.conf
pi@raspberrypi:~/work/aloha $ sudo nano /etc/systemd/system/bluetooth.service.d/01-disable-sap-plugin.conf
    - pybluez: 
        - sudo apt-get install libbluetooth-dev
        - sudo apt-get install python3-dev
        - python3 -m pip install PyBluez
        - python3 -m pip install pygattlib
    - nmap
- [-] verify ssl is disabled for https requests - security vulnerability
- [-] yaml based routine configuration
- [-] build a gui or expose an API - should contain configurations for groups/scenes based on events, as well as timeout behavior

