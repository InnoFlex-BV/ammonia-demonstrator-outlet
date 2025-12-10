import serial
import time
import sys
sys.path.append('/home/innoflex/ammonia-demonstrator-outlet')
# from common_config import create_device, clear_RS485, strong_clear_RS485
from calculate_CRC import calc_crc


""" using manual hex """
def hex_to_bytes(hex_string):
    hex_string = hex_string.replace(" ", "").replace("\n", "") # remove space & new-line
    return bytes.fromhex(hex_string) # hex->bytes: for example, 01->0x01

ser = serial.Serial('/dev/ttyACM0', 9600, bytesize=8, parity=serial.PARITY_NONE, stopbits=1, timeout=1)
ser.reset_input_buffer()
ser.reset_output_buffer()
time.sleep(0.05)

req_hex_1 = "00 10 00 00 00 01 02 00 23"   # broadcast change address to 35(hex=23)
req_hex_2 = "00 03 00 00 00 01" # read device address
req_hex_3 = "32 01 00 00 00 03" # read device status
req_hex_4 = "23 0F 00 00 00 08 01 FF" # turn on all relays
req_hex_5 = "23 0F 00 00 00 08 01 00" # turn off all relays
req_hex_6 = "23 05 00 00 FF 00" # turn on relay 1
req_hex_7 = "23 05 00 00 00 00" # turn off relay 1
request = hex_to_bytes(req_hex_5) # turn into bytes
request += calc_crc(request)

print("Sending HEX:", request.hex(" ").upper())

ser.reset_input_buffer()
ser.reset_output_buffer()
time.sleep(0.05)

ser.write(request)
ser.flush()
time.sleep(0.2)

response = ser.read(11)
print("Response HEX:", response.hex(" ").upper())
ser.close()


""" using serial """
# ser = serial.Serial('/dev/ttyACM0', 9600, bytesize=8, parity=serial.PARITY_NONE, stopbits=1, timeout=1)
# ser.reset_input_buffer()
# ser.reset_output_buffer()
# time.sleep(0.05)
# request = bytes([0x00, 0x10, 0x00, 0x00, 0x00, 0x01, 0x02, 0x00, 0x32]) # change slave address to 35 using broadcast
# # request = bytes([0x00, 0x03, 0x00, 0x00, 0x00, 0x01])
# request += calc_crc(request) # add crc

# ser.reset_input_buffer()
# ser.reset_output_buffer()
# time.sleep(0.05)

# ser.write(request)
# ser.flush()
# time.sleep(0.2)

# response = ser.read(11)
# print("Response:", response)
# ser.close()


""" using minimalmodbus RTU """
# relay = create_device(slave_address=35)
# relay.debug = True
# print("1.5")
# relay.serial.timeout = 1
# print("2")
# #clear_RS485(relay)
# strong_clear_RS485(relay)
# time.sleep(0.5)
# print("3")
# print(f"device address {relay.address}")

# try:
#     #clear_RS485(relay)
#     strong_clear_RS485(relay)
#     print("4")
#     print(f"before write - port open {relay.serial.is_open}")
#     print(f"before write - in_waiting {relay.serial.in_waiting}")
#     relay.write_bit(registeraddress=0, value=0, functioncode=5) # turn relay 1
#     time.sleep(0.2)
#     print("change finished")

# except Exception as e:
#     print("change failed", e)
#     print(f"Error type: {type(e).__name__}")
# finally:
#     clear_RS485(relay)
#     #strong_clear_RS485(relay)