import time
import json
import struct
import minimalmodbus
import sys
sys.path.append('/home/innoflex/ammonia-demonstrator-outlet')
from common_config import create_client, create_device, strong_clear_RS485, serial_lock



class MultiRelayControl:
    def __init__(self, slave_address=35, mqtt_topic = "master/bypass/relay_bypass", client = None):
        # create an object
        self.slave_address = slave_address
        self.relay = None
        self.lock = serial_lock
        self.old_status = [0,0,0]
        self.new_status = None

        minimalmodbus.DEBUG = True

        # MQTT settings
        if client is None:
            self.client = create_client()
            self.client.loop_start()
        else:
            self.client = client

        self.topic = mqtt_topic
        self.client.message_callback_add(self.topic, self.on_message)
        self.client.subscribe(self.topic)


    def relay_initialization(self):
        self.relay = create_device(self.slave_address)
        self.relay.serial.timeout = 1
        with self.lock:
            for reg in range(3):
                strong_clear_RS485(self.relay)
                self.relay.write_bit(registeraddress=reg, value=0, functioncode=5)
        time.sleep(0.25)
        print("Relay initialization finished. Current status: OFF")


    def on_message(self, client, userdata, msg):
        try:
            payload_str = msg.payload.decode().strip()
            print("Received raw payload:", payload_str)

            status_list = json.loads(payload_str)

            if not isinstance(status_list, list) or len(status_list)!=3:
                print("Invalid payload (must with 3 items):", status_list)
                return
            
            if any(value not in [0,1] for value in status_list):
                print("Invalid values (must be 0 or 1):", status_list)
                return
            
            self.new_status = status_list
            print(f"[Bypass Relay] received new status: {self.new_status}")

        except Exception as e:
            print(f"Error: {e}")
        
    def relay_control(self):
        if self.relay is None:
            print("[Bypass Relay] Relay is not initialized.")
            return
        if self.new_status is None:
            return
        
        if self.new_status == self.old_status:
            return

        with self.lock:
            try:
                strong_clear_RS485(self.relay)
                self.relay_vacuum() # vacuum the by-pass line
                for ch in range(3):
                    new_value = self.new_status[ch]
                    old_value = self.old_status[ch]

                    if new_value != old_value:
                        self.relay.write_bit(registeraddress=ch, value=new_value,functioncode=5)
                        time.sleep(1)
                        print(f"[Relay CH{ch+1}] {'ON' if new_value else 'OFF'}")

                self.old_status = self.new_status
            except Exception as e:
                print(f"Relay write error: {e}")


    def relay_vacuum(self):
        vacuum = [0,0,1]
        for ch in range(3):
            self.relay.write_bit(registeraddress=ch, value=vacuum[ch], functioncode=5)
            time.sleep(0.3)
        time.sleep(3)
        self.relay.write_bit(registeraddress=0x0002, value=False, functioncode=5)
        time.sleep(0.2)
        print("By-pass Line has been vacuumed")
    

    def relay_close(self):
        with self.lock:
            strong_clear_RS485(self.relay)
            payload = struct.pack('>HHB', 0, 8, 1) + bytes([0x00])
            self.relay._perform_command(functioncode=15, payload_to_slave=payload)
            print("[Bypass Relay] Relay OFF")

        self.client.loop_stop()
        self.client.disconnect()


    def motor_run(self):
        with self.lock:
            strong_clear_RS485(self.relay)
            self.relay.write_bit(registeraddress=3, value=1, functioncode=5) # CH4 -> vacuum pump motor
            print("[Vacuum Pump] Vacuum Pump motor ON")
    

    def motor_stop(self):
        with self.lock:
            strong_clear_RS485(self.relay)
            self.relay.write_bit(registeraddress=3, value=0, functioncode=5)
            print("[Vacuum Pump] Vacuum Pump motor ON")


    
