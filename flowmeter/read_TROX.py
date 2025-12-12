from common_config import create_client, clear_RS485,serial_lock
import time

def read_flowmeter(device,client = None):
        TROX = device
        if client is None:
                client = create_client()

        with serial_lock:
                clear_RS485(TROX)
                flowrate = TROX.read_register(registeraddress=7, functioncode=4)
                clear_RS485(TROX)

        time.sleep(0.1) # avoid conflict with other devices in RS485 communication
        client.publish("slave/outlet/flowrate", flowrate)
        print(f"[Flowmeter] Flowrate: {flowrate} m3/h")
