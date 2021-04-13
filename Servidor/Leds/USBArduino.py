#!/usr/bin/env python3
import serial
import time


if __name__ == '__main__':
    ser = serial.Serial('/dev/ttyACM0', 115200, timeout=1)
    ser.flush()
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip()
            print(line)
            time.sleep(3)
            ser.write("cat:\n".encode('utf-8'));
            