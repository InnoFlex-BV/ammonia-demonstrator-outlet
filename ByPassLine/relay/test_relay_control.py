import time
import sys
sys.path.append('/home/innoflex/ammonia-demonstrator-outlet')
import minimalmodbus
import serial

""" using minimalmodbus RTU """
relay = minimalmodbus.Instrument('/dev/ttyACM0', 35)  # current slave address
relay.serial.baudrate = 9600
relay.serial.bytesize = 8
relay.serial.parity   = serial.PARITY_NONE
relay.serial.stopbits = 1
relay.serial.timeout  = 0.5
relay.mode = minimalmodbus.MODE_RTU


relay.debug = True
print("1.5")
relay.serial.timeout = 1
print("2")
# strong_clear_RS485(relay) # or mormal clear_RS485
# time.sleep(0.5)
# print("3")
print(f"relay address {relay.address}")

try:
    #clear_RS485(relay)
    # strong_clear_RS485(relay)
    print("4")
    relay.write_bit(registeraddress=0x0000, value=False, functioncode=5) # turn relay 1
    time.sleep(0.2)
    relay.write_bit(registeraddress=0x0001, value=True, functioncode=5) # turn relay 2
    time.sleep(0.2)
    relay.write_bit(registeraddress=0x0002, value=True, functioncode=5) # turn relay 3
    time.sleep(0.2)
    print("change finished")

except Exception as e:
    print("change failed", e)
    print(f"Error type: {type(e).__name__}")
finally:
    # clear_RS485(relay)
    #strong_clear_RS485(relay)
    print("finished")