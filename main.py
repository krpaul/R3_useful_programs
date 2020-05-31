import wiringpi
import threading
import sys, signal
import smbus
import serial
import pynmea2
from HamShieldPy import HamShield
import os
from os import listdir
from os.path import isfile, join
from subprocess import Popen, PIPE
import time
import subprocess
from aprslib import *

# radio settings
vehicle_callsign = 'VE6AZX-11'
radio_freq_aprs = 144390
radio_freq_aux = 145600
radio_tone_aux = 110.9
nCS = 0
clk = 3
dat = 2
mic = 1

# gps settings
#main_gps_port = serial.Serial('/dev/serial0', baudrate = 9600, timeout = 0.5)
#backup_gps_port = serial.Serial('/dev/ttyUSB0', baudrate = 9600, timeout = 0.5)

# state variables

class Relay():
    global bus

    def __init__(self):
        self.DEVICE_ADDRESS = 0x20  # 7 bit address (will be left shifted to add the read write bit)
        self.DEVICE_REG_MODE1 = 0x06
        self.DEVICE_REG_DATA = 0xff
        bus.write_byte_data(self.DEVICE_ADDRESS, self.DEVICE_REG_MODE1, self.DEVICE_REG_DATA)

    def ON_1(self):
        print('ON_1...')
        self.DEVICE_REG_DATA &= ~(0x1 << 0)
        bus.write_byte_data(self.DEVICE_ADDRESS, self.DEVICE_REG_MODE1, self.DEVICE_REG_DATA)

    def ON_2(self):
        print('ON_2...')
        self.DEVICE_REG_DATA &= ~(0x1 << 1)
        bus.write_byte_data(self.DEVICE_ADDRESS, self.DEVICE_REG_MODE1, self.DEVICE_REG_DATA)

    def ON_3(self):
        print('ON_3...')
        self.DEVICE_REG_DATA &= ~(0x1 << 2)
        bus.write_byte_data(self.DEVICE_ADDRESS, self.DEVICE_REG_MODE1, self.DEVICE_REG_DATA)

    def ON_4(self):
        print('ON_4...')
        self.DEVICE_REG_DATA &= ~(0x1 << 3)
        bus.write_byte_data(self.DEVICE_ADDRESS, self.DEVICE_REG_MODE1, self.DEVICE_REG_DATA)

    def OFF_1(self):
        print('OFF_1...')
        self.DEVICE_REG_DATA |= (0x1 << 0)
        bus.write_byte_data(self.DEVICE_ADDRESS, self.DEVICE_REG_MODE1, self.DEVICE_REG_DATA)

    def OFF_2(self):
        print('OFF_2...')
        self.DEVICE_REG_DATA |= (0x1 << 1)
        bus.write_byte_data(self.DEVICE_ADDRESS, self.DEVICE_REG_MODE1, self.DEVICE_REG_DATA)

    def OFF_3(self):
        print('OFF_3...')
        self.DEVICE_REG_DATA |= (0x1 << 2)
        bus.write_byte_data(self.DEVICE_ADDRESS, self.DEVICE_REG_MODE1, self.DEVICE_REG_DATA)

    def OFF_4(self):
        print('OFF_4...')
        self.DEVICE_REG_DATA |= (0x1 << 3)
        bus.write_byte_data(self.DEVICE_ADDRESS, self.DEVICE_REG_MODE1, self.DEVICE_REG_DATA)

    def ALLON(self):
        print('ALL ON...')
        self.DEVICE_REG_DATA &= ~(0xf << 0)
        bus.write_byte_data(self.DEVICE_ADDRESS, self.DEVICE_REG_MODE1, self.DEVICE_REG_DATA)

    def ALLOFF(self):
        print('ALL OFF...')
        self.DEVICE_REG_DATA |= (0xf << 0)
        bus.write_byte_data(self.DEVICE_ADDRESS, self.DEVICE_REG_MODE1, self.DEVICE_REG_DATA)

radio = HamShield(nCS, clk, dat, mic)
#bus = smbus.SMBus(1)
#relay = Relay()
    
def init_radio():
    print 'starting radio setup'
    radio.initialize()

    print 'testing radio connection'

    if (radio.testConnection()):
        print 'radio connection ok'
    else:
        print 'radio connection failed'

    print 'set default radio configuration'
    
    radio.setSQOff()
    freq = radio_freq_aprs
    radio.frequency(144390)
    radio.setModeReceive()
    radio.setRfPower(0)

    print 'radio ready'

def init_relay():
    print 'setting all relays to OFF'
    relay.ALLOFF()

def check_and_return_afsk_packet():
    files = [f for f in listdir('/home/pi/RX/') if isfile(join('/home/pi/RX/', f))]
    if files == []:
        return None
    else:
        fi = open('/home/pi/RX/'+files[0],'r')
        line = fi.readline()
        print 'll'+line
        fi.close()
        os.remove('/home/pi/RX/'+files[0])
        print 'AFSK modem received packet: ' + line
        return line

def send_afsk_packet(packet, freq):
    radio.frequency(freq)
    radio.setModeTransmit()
    fo = open('/home/pi/TX/'+'fo','w+')
    fo.write(packet)
    fo.close()
    time.sleep(3)
    radio.setModeReceive()

def send_dtmf_tones(tones, freq):
    radio.frequency(freq)
    radio.setModeTransmit()
    fo = open('/home/pi/TX/'+'fo','w+')
    fo.write(vehicle_callsign+'>DTMF:')
    for tone in tones:
        fo.write(str(tone))
    fo.close()
    time.sleep(2)
    radio.setModeReceive()

def parseGPSPrimary(str):
    if str.find('GGA') > 0:
        msg = pynmea2.parse(str)
        print "Timestamp: %s -- Lat: %s %s -- Lon: %s %s -- Altitude: %s %s -- Satellites: %s" % (msg.timestamp,msg.lat,msg.lat_dir,msg.lon,msg.lon_dir,msg.altitude,msg.altitude_units,msg.num_sats)

def parseGPSSecondary(str):
    if str.find('GGA') > 0:
        msg = pynmea2.parse(str)
        print "Timestamp: %s -- Lat: %s %s -- Lon: %s %s -- Altitude: %s %s -- Satellites: %s" % (msg.timestamp,msg.lat,msg.lat_dir,msg.lon,msg.lon_dir,msg.altitude,msg.altitude_units,msg.num_sats)

 
if __name__ == '__main__':
    print 'starting direwolf soundmodem'
    dwproc = subprocess.Popen('direwolf')
    time.sleep(2)
    
    print 'starting kiss util'
    kiproc = subprocess.Popen(['kissutil','-o', 'RX','-f','TX'])
    time.sleep(2)
    
    init_radio()
    
    send_dtmf_tones([1,2,3,1,2,3],radio_freq_aprs)
    send_afsk_packet(vehicle_callsign+'>APDR15,WIDE1-1:=3807.41N/212006.78WbMESSAGE',radio_freq_aprs)

    while (True):
        #parseGPSPrimary(main_gps_port.readline())
        #parseGPSSecondary(backup_gps_port.readline())
       
        pkt = check_and_return_afsk_packet()
        if pkt != None:
            if '123#' in pkt:
                relay.ALLON()
                break
        #send_afsk_packet(vehicle_callsign+'>APDR15,WIDE1-1:=3807.41N/212006.78WbMESSAGE',radio_freq_aprs)

    os.killpg(os.getpgid(kiproc.pid), signal.SIGTERM)
    os.killpg(os.getpgid(dwproc.pid), signal.SIGTERM)
    exit()

