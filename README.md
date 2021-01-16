# ALOHA
Built with [raspberry-pi](https://www.raspberrypi.org/).
Aloha is a tool to automate Philips hue light behavior based on external inputs. 
Current capabilities include (with more to come):
- home/away behavior for a single mobile device (light behavior based on device connection to network)
- "theater mode" for vizio devices (light behavior based on tv power state, input selection)

## Getting Started
### Pre-requisites
- python3.6+

### Setup
- update `config.yml` to include your mobile device's IP address
- run `python3 aloha.py` and follow prompts in the terminal

## Development
- dev guide to come

### Contributors
For anybody interested in contributing, feel free to create issues/open a PR


## TODOS
- [-] ssl is disabled for https requests - security vulnerability
- [-] build a gui or expose an API - should contain configurations for groups/scenes based on events, as well as timeout behavior
- [-] update script