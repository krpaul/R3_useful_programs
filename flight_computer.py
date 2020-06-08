#!/user/bin/env python3
import time, serial, pynmea2 as nmea, subprocess

def take_photo():
    filename = t.strftime('%x_%X').replace("/", "-")
    cmd = f"raspistill -vf -o ./pics/{filename}.jpeg"
    subprocess.call(cmd, shell=True)

def send_gps_data(lat, lng, alt):
    print("GPS Data: ", lat, lng, alt)

def main():
    ser = serial.Serial(
        port='/dev/ttyS0',
        baudrate = 9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1
    )

    data = None
    CAM_INTERVAL = 5
    MAIN_INTERVAL = 1

    interval_count = 0
    while True:
        line = str(ser.readline(), 'utf-8').strip()
        if "GPGGA" in line:
            data = nmea.parse(line)
            send_gps_data(data.latitude, data.longitude, data.altitude)

        if interval_count >= CAM_INTERVAL:
            interval_count -= CAM_INTERVAL
            take_photo()

        interval_count += MAIN_INTERVAL
        time.sleep(MAIN_INTERVAL)

main()