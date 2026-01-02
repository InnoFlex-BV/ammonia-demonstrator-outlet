import paho.mqtt.client as mqtt
import subprocess
import signal
import os
import time


broker_ip = "ammonia-master.local"
topic_control = "master/outlet/control"
topic_status = "slave/outlet/status"
main_script_path  = "/home/innoflex/ammonia-demonstrator-outlet/main_module.py"

outlet_process = None


def on_message(client, userdata, msg):
    global outlet_process
    command = msg.payload.decode().upper()

    if command == "START":
        if outlet_process is None or outlet_process.poll() is not None:
            print("Starting main_module.py ...")
            outlet_process = subprocess.Popen(["python3", main_script_path])
            client.publish(topic_status, "RUNNING", retain=True)

    elif command == "STOP":
        if outlet_process and outlet_process.poll() is None:
            print("Stopping main_module.py ...")
            outlet_process.send_signal(signal.SIGINT)
            outlet_process.wait()
            outlet_process = None
            client.publish(topic_status, "STOPPED", retain=True)
            print("Outlet Module Stopped")

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe(topic_control)
    client.publish(topic_status, "STOPPED", retain=True)

"""initialize MQTT"""
client = mqtt.Client(client_id="OutletPi_manager")
client.on_connect = on_connect
client.on_message = on_message

client.will_set(topic_status, "OFFLINE", retain=True) # in case of that outlet_pi is not working
client.connect(broker_ip, 1883, 60)

client.loop_forever()
