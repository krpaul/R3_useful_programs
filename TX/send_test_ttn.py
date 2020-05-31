"""
Example for using the RFM9x Radio with Raspberry Pi and LoRaWAN

Learn Guide: https://learn.adafruit.com/lora-and-lorawan-for-raspberry-pi
Author: Brent Rubell for Adafruit Industries
"""
import threading
import time
import subprocess
import busio
from digitalio import DigitalInOut, Direction, Pull
import board
# Import Adafruit TinyLoRa
from adafruit_tinylora.adafruit_tinylora import TTN, TinyLoRa


# TinyLoRa Configuration
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
cs = DigitalInOut(board.CE1)
irq = DigitalInOut(board.D22)
rst = DigitalInOut(board.D25)

# TTN Device Address, 4 Bytes, MSB
devaddr = bytearray([ 0x26, 0x02, 0x18, 0xD7 ])
# TTN Network Key, 16 Bytes, MSB
nwkey = bytearray([ 0xE6, 0xA9, 0x3B, 0x39, 0xF4, 0x92, 0xE0, 0xFF, 0x44, 0x1C, 0x89, 0xCC, 0x01, 0x91, 0xC9, 0x00 ])
# TTN Application Key, 16 Bytess, MSB
app = bytearray([ 0x4E, 0xF0, 0xFE, 0x88, 0xE3, 0xCD, 0x1F, 0xD3, 0x94, 0x9C, 0x17, 0xD6, 0x83, 0x6D, 0xB5, 0x76 ])

# Initialize ThingsNetwork configuration
ttn_config = TTN(devaddr, nwkey, app, country='US')
# Initialize lora object
lora = TinyLoRa(spi, cs, irq, rst, ttn_config)
# 2b array to store sensor data
data_pkt = None
# time to delay periodic packet sends (in seconds)
data_pkt_delay = 5.0

def send_pi_data_periodic():
    threading.Timer(data_pkt_delay, send_pi_data_periodic).start()
    print("Sending periodic data...")
    send_pi_data(CPU)
    print('CPU:', CPU)

def send_pi_data(data):
    # Encode 
    data_pkt = bytearray(CPU, 'utf-8')
    # Send data packet
    lora.send_data(data_pkt, len(data_pkt), lora.frame_counter)
    lora.frame_counter += 1
    print('Data sent!')
    time.sleep(0.5)

while True:
    packet = None
    # draw a box to clear the image

    # read the raspberry pi cpu load
    # cmd = "top -bn1 | grep load | awk '{printf \"%.1f\", $(NF-2)}'"
    # CPU = subprocess.check_output(cmd, shell = True )
    # CPU = float(CPU)

    CPU = "HELLO RENERT"
    send_pi_data(CPU)

    time.sleep(3)
