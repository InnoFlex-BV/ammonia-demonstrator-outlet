import minimalmodbus
import time


TROX = minimalmodbus.Instrument('/dev/ttyACM0', 7)
TROX.serial.baudrate = 9600
TROX.serial.bytesize = 8
TROX.serial.parity = minimalmodbus.serial.PARITY_NONE
TROX.serial.stopbits = 1
TROX.serial.timeout = 1
TROX.mode = minimalmodbus.MODE_RTU


## read input & holding registers
print("Registers: \n")
regs = list(range(6, 8)) + [10,11] + list(range(50, 54)) + list(range(99, 104)) + [107,109,110,112,113,124,126]
for reg in regs:
    try:
        value = TROX.read_register(registeraddress=reg, functioncode=3)
        print(f"Register No.{reg+1} | Address {reg:02d}: {value}")
        time.sleep(0.1)
    except Exception as e:
        print(f"Register No.{reg+1} | Address {reg:02d}: Error -> {e}")
        break


# print("\n Holding Registers: \n")

# address = TROX.read_register(registeraddress=0x0100, functioncode=3)
# print(f"Holding Register 0x0100 | Slave address: {address}")
# time.sleep(0.1)

# baudrate_mode = TROX.read_register(registeraddress=0x0101, functioncode=3)
# baudrate_table = {1:1200,2:2400,3:4800,4:9600,5:19200,6:115200}
# print(f"Holding Register 0x0101 | Baudrate: {baudrate_table.get(baudrate_mode,'Unknown')}")


print("\n Done.")