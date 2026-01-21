import time
from common_config import create_client, create_device
from sensor.read_HG803 import read_sensor as read_HG803
from flowmeter.read_TROX import read_flowmeter
from fan.fan_control import FanControll
from ByPassLine.sensor.read_ammonia import read_sensor as read_ammonia
from ByPassLine.MultiRelay.multi_relay_control import MultiRelayControl


mqtt_client = create_client()
mqtt_client.loop_start()

""" create objects """
fan_out = None
HG803_sensor = create_device(slave_address=3)
TROX_flowmeter = create_device(slave_address=9)

AmmoSensor1 = create_device(slave_address=37)
AmmoSensor2 = create_device(slave_address=38)
multi_relay = None



try:

    """  initializations of devices """
    fan_out = FanControll(slave_address=4, mqtt_topic="master/outlet/fan_out", client = mqtt_client)
    fan_out.fan_initialzation()
    time.sleep(1)
    multi_relay = MultiRelayControl(slave_address=35, mqtt_topic="master/bypass/relay_bypass", client=mqtt_client)
    multi_relay.relay_initialization()
    multi_relay.motor_run()
    time.sleep(1)
    print("Outlet module: Initialization finished")


    """  start multi thread """
    tasks = [
        {"name": "HG803 Sensor", "func": lambda: read_HG803(device=HG803_sensor, client=mqtt_client), "interval": 3, "next_run": 0},
        {"name": "Flowmeter", "func": lambda: read_flowmeter(device=TROX_flowmeter, client=mqtt_client), "interval":6, "next_run":0},
        {"name": "Fan Control", "func": fan_out.fan_control, "interval": 5, "next_run": 0},
        {"name": "Ammonia Sensor 1", "func": lambda: read_ammonia(device=AmmoSensor1, client=mqtt_client, mqtt_topic="slave/bypass/ammonia_ppm_1", label="(inlet)"), "interval": 5, "next_run": 0},
        {"name": "Ammonia Sensor 2", "func": lambda: read_ammonia(device=AmmoSensor2, client=mqtt_client, mqtt_topic="slave/bypass/ammonia_ppm_2", label="(outlet)"), "interval": 5, "next_run": 0},
        {"name": "Bypass-line Relay", "func": multi_relay.relay_control, "interval":5, "next_run":0},
    ]


    while True:
        now = time.time()
        for t in tasks:
            if now  >= t["next_run"]:
                try:
                    t["func"]()
                except Exception as e:
                    print(f"Error in [{t['name']}]. Task {t['func'].__name__ } error: {e}")
                t["next_run"] = now + t["interval"]
        time.sleep(0.01)

except KeyboardInterrupt:
    print("\n Exiting programm due to keyboard interrupt...")

except Exception as e:
    print(f"\nExiting program due to error: {e}")

finally:
    # cleanup all devices in RS485
    if fan_out is not None:
        try:
            fan_out.fan_stop()
        except Exception as e:
            print(f"Error stopping fan: {e}")

    if multi_relay is not None:
        try:
            multi_relay.motor_stop()
            multi_relay.relay_close()
        except Exception as e:
            print(f"Error closing relay bypass: {e}")

    print("All devices cleaned up.")