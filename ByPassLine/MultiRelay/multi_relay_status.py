import minimalmodbus
from time import sleep


device = minimalmodbus.Instrument('/dev/ttyACM0', 35)
device.serial.baudrate = 9600
device.serial.bytesize = 8
device.serial.parity = minimalmodbus.serial.PARITY_NONE
device.serial.stopbits = 1
device.serial.timeout = 1
device.mode = minimalmodbus.MODE_RTU
# device.debug = True



# change settings
print("Relay status \n")
for reg in range(0,8):
    try:
        value = device.read_bits(registeraddress=reg, number_of_bits=1, functioncode=1)
        print(f"Relay {reg+1}: {'ON' if value[0] else 'OFF'}")
    except Exception as e:
        print(f"Relay {reg+1} | Error -> {e}")
        break

print("\n Done.")