#import PySerial
import serial
import time

class ArduinoUSB(object):
	def __init__(self):
		# default settings
		self.ser = serial.Serial()
		self.ser.baudrate = 19200
		self.ser.port = "/dev/ttyACM0"
		self.ser.timeout = 1 #seconds before giving up on read/write operations
	
	def connect(self):
		if self.ser.isOpen() == False:
			self.ser.open()
			time.sleep(1) #need to wait for connection to "warm up" before messages can be sent (why?)
	
	def write(self, msg):
		if self.ser.isOpen() == False:
			self.connect()
		if self.ser.isOpen():
			try:
				self.ser.write(msg)
				if str(msg) == "1\n":
					print("told Arduino to START imaging")
				if str(msg) == "0\n":
					print("told Arduino to STOP imaging")
			except:
				print("could not write to Arduino?")
	
	def __del__(self):
		if self.ser.isOpen():
			print("closing serial connection to Arduino")
			self.ser.close()
