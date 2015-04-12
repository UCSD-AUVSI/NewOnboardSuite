import serial
import sys
import threading
from time import sleep

if len(sys.argv) <= 1:
	print("usage:  {serial-port}")
	quit()
serialPortStr = str(sys.argv[1])

try:
	ser = serial.Serial(serialPortStr, baudrate=19200, timeout=1, writeTimeout=1)
except:
	print("error: could not connect to serial on that port")
	quit()

print("connected to \""+ser.name+"\"")

sleep(2)

byteswritten = ser.write("1\n")
print("(1) byteswritten == "+str(byteswritten))

sleep(5)

byteswritten = ser.write("0\n")
print("(0) byteswritten == "+str(byteswritten))

while True:
	line = ser.readline()   # read a '\n' terminated line
	if len(line) > 0:
		print("read message: \""+str(line)+"\"")
	else:
		break

ser.close()             # close port

