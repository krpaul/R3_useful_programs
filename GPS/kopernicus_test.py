import tsip
import serial

# Open serial connection to Copernicus II receiver
serial_conn = serial.Serial('/dev/ttyS0', 38400)
gps_conn = tsip.GPS(serial_conn)

# Prepare and send command packet 0x21
command = tsip.Packet(0x21)
gps_conn.write(command)

while True:      # should implement timeout here!!!
    report = gps_conn.read()
    if report[0] == 0x41:
        print( 'GPS time of week .......: %f' % (report[1]))
        print( 'Extended GPS week number: %d' % (report[2]))
        print( 'GPS UTC offset .........: %f' % (report[3]))
        break
