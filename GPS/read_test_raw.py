#!/user/bin/env python3
import time, serial#, pynmea2 as nmea

ser = serial.Serial(
      port='/dev/ttyAMA0', #Replace ttyS0 with ttyAM0 for Pi1,Pi2,Pi0
      baudrate = 4800,
      parity=serial.PARITY_NONE,
      stopbits=serial.STOPBITS_ONE,
      bytesize=serial.EIGHTBITS,
      timeout=1
)

data = None
while True:
    rl = ser.readline()
    try:
        print(str(rl, 'utf-8'))
    except:
        print(rl)
