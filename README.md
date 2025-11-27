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
