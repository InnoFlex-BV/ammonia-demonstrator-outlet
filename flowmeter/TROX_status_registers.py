import minimalmodbus
import time


TROX = minimalmodbus.Instrument('/dev/ttyACM0', 9)
TROX.serial.baudrate = 9600
TROX.serial.bytesize = 8
TROX.serial.parity = minimalmodbus.serial.PARITY_NONE
TROX.serial.stopbits = 1
TROX.serial.timeout = 2
TROX.mode = minimalmodbus.MODE_RTU


## read input & holding registers
print("Registers: \n")
regs = list(range(6, 8)) + [10,11] + list(range(50, 54)) + list(range(99, 104)) + [107,109,110,112,113,124,126]
for reg in regs:
    try:
        value = TROX.read_register(registeraddress=reg, functioncode=4)
        print(f"Register No.{reg+1} | Address {reg:02d}: {value}")
        time.sleep(0.1)
    except Exception as e:
        print(f"Register No.{reg+1} | Address {reg:02d}: Error -> {type(e).__name__}: {e}")
        break


print("\n Done.")