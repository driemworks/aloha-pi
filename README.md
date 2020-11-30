# ALOHA
Built with [raspberry-pi](https://www.raspberrypi.org/).
Aloha is a tool to automate Philips hue light behavior based on external inputs. 
Current capabilities include (with more to come):
- home/away behavior for a single mobile device (light behavior based on device connection to network)
- "theater mode" for vizio devices (light behavior based on tv power state, input selection)

## Getting Started
### Pre-requisites
- use python3.6+
- install nmap, enable bluetooth (guide to come)

### Setup
- update `config.yml` to include your mobile device's IP address
- run `python3 aloha.py` and follow prompts in the terminal

## Development
- dev guide to come

### Contributors
For anybody interested in contributing, feel free to create issues/open a PR


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
- [-] ssl is disabled for https requests - security vulnerability
- [-] build a gui or expose an API - should contain configurations for groups/scenes based on events, as well as timeout behavior
