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


try:
    while True:
        for ch in range(0,3):
            device.write_bit(registeraddress=ch, value=1, functioncode=5)
            sleep(1)
        sleep(3)
        for ch in range(0,3):
            device.write_bit(registeraddress=ch, value=0, functioncode=5)
            sleep(1)
        sleep(3)


except Exception as e:
    print(f"{type(e).__name__}: {e}")
    sleep(0.1)


except KeyboardInterrupt:
   try:
    for ch in range(0, 3):
            device.write_bit(registeraddress=ch, value=0, functioncode=5) 
    print("Keyboard Interrupt")
   except:
       pass

finally:
    print("\n Done.")