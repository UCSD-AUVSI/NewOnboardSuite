import serial
import time
import threading
from networking_to_ground.send_message_to_ground import send_message_to_ground
import json
from telem_listener import globalvar_connection_gps_telem as GPSTelem
from collections import deque

class ArduinoUSB(object):
	def __init__(self):
		# default settings
		self.ser = serial.Serial()
		self.ser.baudrate = 19200
		self.ser.port = "/dev/ttyACM0"
		self.ser.timeout = 1 #seconds before giving up on read/write operations
		self.tryingtoautoconnect = False
		self.ispolling = False
		self.gps_queue = deque([])

	def private___tryconnect(self):
		if self.ser.isOpen() == False:
			keeptrying = True
			while keeptrying:
				if self.ser.port == "/dev/ttyACM0":
					self.ser.port = "/dev/ttyACM1"
				else:
					self.ser.port = "/dev/ttyACM0"

				try:
					self.ser.open()
					time.sleep(1) #need to wait for connection to "warm up" before messages can be sent (why?)
					keeptrying = False
					self.StartPolling()
				except serial.serialutil.SerialException:
					print("waiting for Arduino to be connected")
					keeptrying = True
					time.sleep(1)
		self.tryingtoautoconnect = False

	def CheckConnectionBoolean(self):
		if self.ser.isOpen():
			return True
		return False

	def CheckWriteability(self):
		if self.ser.isOpen():
			if self.write("g\n") == True:
				return "connected-and-can-write"
			else:
				return "error-writing"
		return "NOT-connected"

	def threadedconnect(self):
		if self.tryingtoautoconnect == False and self.ser.isOpen() == False:
			self.tryingtoautoconnect = True
			self.mythread = threading.Thread(target=self.private___tryconnect)
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
				if str(msg) == "g\n":
					print("told Arduino to return status in response to query")
				return True
			except:
				print("could not write to Arduino?")
		return False

	def __del__(self):
		if self.ser.isOpen():
			print("closing serial connection to Arduino")
			self.ser.close()

	def StartPolling(self):
		if self.ispolling == False:
			self.ispolling = True
			self.mythread = threading.Thread(target=self.private___PollArduinoContinuously)
			self.mythread.daemon = True
			self.mythread.start()

	def private___PollArduinoContinuously(self):
		print("STARTING TO POLL ARDUINO CONTINUOUSLY")
		while True:
			time.sleep(0.1)
			while self.CheckConnectionBoolean() == True:
				readmsg = str(self.ser.readline())
				if readmsg == "1\n":
					send_message_to_ground(json.dumps({"cmd":"status","args":{"arduino":"is-shooting"}}))
				elif readmsg == "0\n":
					send_message_to_ground(json.dumps({"cmd":"status","args":{"arduino":"is-NOT-shooting"}}))
				elif readmsg == "s\n":
					# image taken, save most recent gps into queue
					self.saveGPS()
				else:
					print("UNKNOWN MESSAGE FROM ARDUINO: \'"+readmsg+"\'")
					print("todo: process camera-shoot trigger messages")
				time.sleep(0.001)
		self.ispolling = False

	def saveGPS(self):
		location = GPSTelem.connection.ask_gps()
		self.gps_queue.append(location)
