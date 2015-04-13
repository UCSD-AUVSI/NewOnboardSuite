import serial
import sys
import threading
from time import sleep

#-----------------------------------------------
# Parse command-line argument

if len(sys.argv) <= 1:
	print("usage:  {serial-port}")
	quit()
serialPortStr = str(sys.argv[1])

#-----------------------------------------------
# Try to connect to Arduino with PySerial

try:
	ser = serial.Serial(serialPortStr, baudrate=19200, timeout=1, writeTimeout=1)
except:
	print("error: could not connect to serial on that port")
	quit()

print("connected to \""+ser.name+"\"")

#-----------------------------------------------
# need to sleep >= 2 seconds while serial connection "warms up" before sending messages to Arduino
#  any messages sent before this won't be received by the Arduino

sleep(2)

#-----------------------------------------------
# Start, then stop, Arduino image-capture triggering

if ser.write("1\n") < 1:
	print("error: could not write message to Arduino")

sleep(5) #capture about 5 images

if ser.write("0\n") < 1:
	print("error: could not write message to Arduino")

#-----------------------------------------------
# Read any messages the Arduino sent back

while True:
	line = ser.readline()   # read a '\n' terminated line
	if len(line) > 0:
		print("read message: \""+str(line)+"\"")
	else:
		break

#-----------------------------------------------
# Close PySerial connection

ser.close()






