#!/usr/bin/env python

import serial
import sys

# Utilities used for file handling and logging
from utilities.file import log_file_name as log_file_name

# NMEA Log File
nmea_log_file_name = '/home/johnoraw/ProjectP/logfiles/' + log_file_name('.nmea')
# Open the file for append
nmea_output_file = open(nmea_log_file_name, 'w', newline='')


print('***** NMEA Logger *****')
print('Accepts NMEA from a serial port:')
print('1. Logs raw data')

try:
    with serial.Serial("/dev/ttySC1") as serial_port:
        serial_port.baudrate = 19200
        serial_port.bytesize = serial.EIGHTBITS
        serial_port.parity = serial.PARITY_NONE
        serial_port.stopbits = serial.STOPBITS_ONE
        serial_port.timeout = None

        while True:
            # Read the first byte, if no byte, loop
            byte1 = serial_port.read(1)
            if len(byte1) < 1:
                break

            # Check for UBX header = xB5 and X62, Unicode = µb
            # Minimal UBX code, just to read the bytes
            if byte1 == b"\xb5":
                byte2 = serial_port.read(1)
                if len(byte2) < 1:
                    break
                if byte2 == b"\x62":
                    # Get the UBX class
                    byte3 = serial_port.read(1)
                    # Get the UBX message
                    byte4 = serial_port.read(1)
                    # Get the UBX payload length
                    byte5and6 = serial_port.read(2)
                    # Calculate the length of the payload
                    length_of_payload = int.from_bytes(byte5and6, "little", signed=False)
                    # Read the buffer for the payload length
                    ubx_payload = serial_port.read(length_of_payload)
                    # Last two bytes are 2*CRC, save them for later use
                    ubx_crc_a = serial_port.read(1)
                    ubx_crc_b = serial_port.read(1)

            # Check for NMEA0183, leading with a $ symbol
            elif byte1 == b"\x24":
                nmea_full_bytes = serial_port.readline()
                nmea_full_string = nmea_full_bytes.decode("latin-1")
                # Check for corrupted lines
                if nmea_full_string.isascii():
                    # If sentence is OK, record it in a logfile
                    nmea_output_file.writelines(nmea_full_string)
                    # Force OS to write each line, not to buffer
                    nmea_output_file.flush()
                    print(f'NMEA: Received {nmea_full_string.strip()}')

except serial.SerialException as err:
    print(f"Terminating with a serial port error: \n {err}")
    sys.exit()
except ValueError as err:
    print(f"Value Error error: {err}")
except OSError as err:
    print(f"OS error: {err}")
except Exception as err:
    print(f"Terminating with an unclassified error: \n {err}")
    sys.exit()
except KeyboardInterrupt:
    print('User has terminated the programme via the keyboard')
    nmea_output_file.close()
    sys.exit()
