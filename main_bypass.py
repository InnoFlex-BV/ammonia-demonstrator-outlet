import time
from common_config import create_client, create_device
from ByPassLine.sensor.read_ammonia import read_sensor as read_ammonia
from ByPassLine.relay.relay_control import RelayControl


mqtt_client = create_client()
mqtt_client.loop_start()

""" create objects """
AmmoSensor1 = create_device(slave_address=37)
AmmoSensor2 = create_device(slave_address=38)
relay_bypass = None



try:

    """  initializations of devices """
    relay_bypass = RelayControl(slave_address=35, mqtt_topic="master/bypass/relay_bypass", client=mqtt_client)
    relay_bypass.relay_initialization()
    time.sleep(1)


    """  start multi thread """
    tasks = [
        {"func": lambda: read_ammonia(device=AmmoSensor1, client=mqtt_client, mqtt_topic="slave/bypass/ammonia_ppm_1", label="(inlet)"), "interval": 5, "next_run": 0},
        {"func": lambda: read_ammonia(device=AmmoSensor2, client=mqtt_client, mqtt_topic="slave/bypass/ammonia_ppm_2", label="(outlet)"), "interval": 5, "next_run": 0},
        {"func": relay_bypass.relay_control, "interval":5, "next_run":0},
    ]


    while True:
        now = time.time()
        for t in tasks:
            if now  >= t["next_run"]:
                t["func"]()
                t["next_run"] = now + t["interval"]
        time.sleep(0.01)

except KeyboardInterrupt:
    print("\n Exiting programm due to keyboard interrupt...")

except Exception as e:
    print(f"\nExiting program due to error: {e}")

finally:
    # cleanup all devices in RS485
    if relay_bypass is not None:
        try:
            relay_bypass.relay_close()
        except Exception as e:
            print(f"Error closing relay bypass: {e}")

    print("All devices cleaned up.")