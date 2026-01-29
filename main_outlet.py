import time
from common_config import create_client, create_device
from sensor.read_HG803 import read_sensor as read_HG803
from flowmeter.read_TROX import read_flowmeter
from fan.fan_control import FanControll


mqtt_client = create_client()
mqtt_client.loop_start()

""" create objects """
fan_out = None
HG803_sensor = create_device(slave_address=3)
TROX_flowmeter = create_device(slave_address=9)



try:

    """  initializations of devices """
    fan_out = FanControll(slave_address=4, mqtt_topic="master/outlet/fan_out", client = mqtt_client)
    fan_out.fan_initialization()
    time.sleep(1)


    """  start multi thread """
    tasks = [
        {"name": "HG803 Sensor", "func": lambda: read_HG803(device=HG803_sensor, client=mqtt_client), "interval": 3, "next_run": 0},
        {"name": "Flowmeter", "func": lambda: read_flowmeter(device=TROX_flowmeter, client=mqtt_client), "interval": 6, "next_run": 0},
        {"name": "Fan Control", "func": fan_out.fan_control, "interval": 5, "next_run": 0},
    ]


    while True:
        now = time.time()
        for t in tasks:
            if now >= t["next_run"]:
                try:
                    t["func"]()
                except Exception as e:
                    print(f"Error in [{t['name']}]: {e}")
                t["next_run"] = now + t["interval"]
        time.sleep(0.01)

except KeyboardInterrupt:
    print("\n Exiting program due to keyboard interrupt...")

except Exception as e:
    print(f"\nExiting program due to error: {e}")

finally:
    # cleanup all devices in RS485
    if fan_out is not None:
        try:
            fan_out.fan_stop()
        except Exception as e:
            print(f"Error stopping fan: {e}")

    print("All devices cleaned up.")