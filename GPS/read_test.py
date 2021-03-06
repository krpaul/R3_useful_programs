#!/user/bin/env python3
import time, serial, pynmea2 as nmea

ser = serial.Serial(
      port='/dev/ttyS0', #Replace ttyS0 with ttyAM0 for Pi1,Pi2,Pi0
      baudrate = 4800,
      parity=serial.PARITY_NONE,
      stopbits=serial.STOPBITS_ONE,
      bytesize=serial.EIGHTBITS,
      timeout=1
)

data = None
while True:
    line = str(ser.readline(), 'utf-8').strip()
    if "GPGGA" in line:
        data = nmea.parse(line)
        print(data.latitude, data.longitude, data.altitude)
        #print(data.__dict__)
  
