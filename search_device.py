import serial, time
from calculate_CRC import calc_crc
from common_config import strong_clear_RS485

def build_read_cmd(addr):
    frame = bytearray([addr, 0x03, 0x00, 0x00, 0x00, 0x01])
    frame += calc_crc(frame)
    return frame


baudrates = [9600, 19200]


try:
    for baud in baudrates:
        print("Testing baud:", baud)
        ser = serial.Serial("/dev/ttyACM0", baud, timeout=1)

        for addr in list(range(30, 40)) + list(range(250, 256)):
            strong_clear_RS485()
            cmd = build_read_cmd(addr)

            ser.reset_input_buffer()
            ser.reset_output_buffer()
            time.sleep(0.05)   

            ser.write(cmd)
            ser.flush()
            time.sleep(0.15)
            
            ser.reset_input_buffer()
            time.sleep(0.05)

            ser.write(cmd)
            ser.flush()
            time.sleep(0.15)        
            
            resp = ser.read(32)

            if resp:
                print(f"Device at addr {addr} with baud {baud}: {resp.hex()}")

        ser.close()
except KeyboardInterrupt:
    print("\n[INFO] KeyboardInterrupt detected, cleaning up RS485...")

    try:
        ser.reset_input_buffer()
        ser.reset_output_buffer()
        ser.flush()
    except:
        pass
    try:
        ser.close()
    except:
        pass
    print("[INFO] RS485 buffers cleared.")