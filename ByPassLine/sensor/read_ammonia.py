from common_config import create_device, create_client, clear_RS485, serial_lock
import time

def read_sensor(device, client = None, mqtt_topic=None):
    if client is None:
        client = create_client()
    
    with serial_lock:
        clear_RS485(device=device)
        values = device.read_registers(registeraddress=0x0000, number_of_registers=5, functioncode=3)
        clear_RS485(device=device)

    time.sleep(0.1)
    Ammo_concentration = values[4]/100
    client.publish(mqtt_topic, Ammo_concentration)
    print(f"[ReadAmmonia] Ammonia concentration: {Ammo_concentration} ppm.")


