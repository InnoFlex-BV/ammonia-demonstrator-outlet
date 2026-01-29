Ammonia Demonstrator Outlet Module

## Recent Changes (2026-01-29)

### Bug Fixes
- Fixed typo `fan_initialzation` -> `fan_initialization` in fan/fan_control.py, main_module.py, main_outlet.py
- Fixed typo `programm` -> `program` in all main files
- Fixed critical bug in main_outlet.py: added missing device parameters for HG803 sensor and TROX flowmeter

### Improvements
- Added error handling for task execution in main_outlet.py and main_bypass.py (prevents single task failure from crashing entire program)
- Added `"name"` field to tasks in main_outlet.py and main_bypass.py for better error reporting

---

## Installation

Websites for instruction of installations on the Raspberry Pi

Node-red:
https://nodered.org/docs/getting-started/raspberrypi

Grafana:
https://grafana.com/tutorials/install-grafana-on-raspberry-pi/

InfluxDB:
https://pimylifeup.com/raspberry-pi-influxdb/

Mosquitto:
https://randomnerdtutorials.com/how-to-install-mosquitto-broker-on-raspberry-pi/

Git:
in the linux terminal:
sudo apt-get install -y git

Pyserial (prerequisite of minimalmodbus):
run these commands in terminal
wget https://github.com/pyserial/pyserial/archive/refs/tags/v3.4.tar.gz
python3 setup.py install --break-system-packages


minimalmodbus:
run these commands in terminal:
wget https://files.pythonhosted.org/packages/source/m/minimalmodbus/minimalmodbus-2.1.1.tar.gz
python3 -m pip install minimalmodbus-2.1.1.tar.gz --break-system-packages
