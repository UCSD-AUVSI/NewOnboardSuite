import serial
import time
import threading

class ArduinoUSB(object):
	def __init__(self):
		# default settings
		self.ser = serial.Serial()
		self.ser.baudrate = 19200
		self.ser.port = "/dev/ttyACM0"
		self.ser.timeout = 1 #seconds before giving up on read/write operations
		self.tryingtoautoconnect = False
	
	def tryconnect(self):
		if self.ser.isOpen() == False:
			keeptrying = True
			while keeptrying:
				try:
					self.ser.open()
					time.sleep(1) #need to wait for connection to "warm up" before messages can be sent (why?)
					keeptrying = False
				except serial.serialutil.SerialException:
					print("waiting for Arduino to be connected")
					keeptrying = True
					time.sleep(1)
		self.tryingtoautoconnect = False
	
	def threadedconnect(self):
		if self.tryingtoautoconnect == False:
			self.tryingtoautoconnect = True
			self.mythread = threading.Thread(target=self.tryconnect)
			self.mythread.daemon = True
			self.mythread.start()
	
	def write(self, msg):
		if self.ser.isOpen() == False:
			self.threadedconnect()
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
