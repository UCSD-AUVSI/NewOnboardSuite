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
		self.possibleSerPortIdxCheck = 0
		self.possibleSerPorts = ["/dev/ttyUSB0", "/dev/ttyUSB1", "/dev/ttyUSB2", "/dev/ttyUSB3", "/dev/ttyACM0", "/dev/ttyACM1", "/dev/ttyACM2", "/dev/ttyACM3"]
		self.ser.timeout = 1 #seconds before giving up on read/write operations
		self.autoconnThread = None
		self.tryingtoautoconnect = False
		self.KeepTryingtoautoconnect = False
		self.trulyConnectedAfterReceivingResponse = False
		self.keeppolling = False
		self.pollingthread = None
		self.gps_dict = {}
                self.images_count = 0
		self.gps_queue = deque([])

	def private___tryconnect(self):
		if self.ser.isOpen() == False:
			printidx = 0
			self.KeepTryingtoautoconnect = True
			while self.KeepTryingtoautoconnect:
				# if we can't find it on USB0, try other USB ports
				self.possibleSerPortIdxCheck += 1
				if self.possibleSerPortIdxCheck == len(self.possibleSerPorts):
					self.possibleSerPortIdxCheck = 0
				self.ser.port = self.possibleSerPorts[self.possibleSerPortIdxCheck]
				try:
					self.ser.open()
					time.sleep(1.1) #need to wait for connection to "warm up" before messages can be sent (why?)
					self.StartPolling()
					print("ArduinoAutoconnect: found serial device at \'"+str(self.ser.port)+"\': "+self.CheckWriteability())
					time.sleep(0.9)
					if self.trulyConnectedAfterReceivingResponse == True:
						self.KeepTryingtoautoconnect = False
						print("ArduinoAutoconnect: found the actual arduino at \'"+str(self.ser.port)+"\': confirmed by response")
					else:
						self.disconnect() #try another serial port, might be the wrong device if we didn't get a response
				except serial.serialutil.SerialException:
					pass
				time.sleep(0.1)
				printidx += 1
				if printidx == 10:
					print("waiting for Arduino to be connected")
					printidx = 0
		self.tryingtoautoconnect = False

	def CheckConnectionBoolean(self):
		if self.ser.isOpen():
			return True
		return False

	def CheckWriteability(self):
		if self.ser.isOpen():
			if self.write("g\n") == True:
				return str(self.ser.port)+": connected-and-can-write"
			else:
				return str(self.ser.port)+": error-writing"
		return "NOT-connected"

	def threadedconnect(self):
		if self.tryingtoautoconnect == False and self.ser.isOpen() == False:
			self.tryingtoautoconnect = True
			self.autoconnThread = threading.Thread(target=self.private___tryconnect)
			self.autoconnThread.daemon = True
			self.autoconnThread.start()
	
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
	
	def disconnect(self):
		self.KeepTryingtoautoconnect = False
		self.autoconnThread.join()
		self.stoppolling()
		if self.ser.isOpen():
			print("closing serial connection to Arduino")
			self.ser.close()
		self.trulyConnectedAfterReceivingResponse = False
	
	def stoppolling(self):
		if self.pollingthread is not None:
			self.keeppolling = False
			self.pollingthread.join()
		self.pollingthread = None
	
	def __del__(self):
		self.disconnect()
	
	def StartPolling(self):
		self.stoppolling()
		while self.pollingthread is not None:
			time.sleep(0.1)
		self.pollingthread = threading.Thread(target=self.private___PollArduinoContinuously)
		self.pollingthread.daemon = True
		self.pollingthread.start()
	
	def private___PollArduinoContinuously(self):
		print("STARTING TO POLL ARDUINO CONTINUOUSLY at "+str(self.ser.port))
		self.keeppolling = True
		readerrs = 0
		while self.keeppolling:
			time.sleep(0.1)
			while self.keeppolling and self.CheckConnectionBoolean() == True:
				readmsg = ""
				try:
					readmsg = str(self.ser.readline())
				except serial.serialutil.SerialException:
					readerrs += 1
					send_message_to_ground(json.dumps({"cmd":"status","args":{"arduino":str(str(self.ser.port)+": "+str(readerrs)+" read errors")}}))
					time.sleep(0.5)
				
				if readmsg == "1\n":
					send_message_to_ground(json.dumps({"cmd":"status","args":{"arduino":str(str(self.ser.port)+": shooting")}}))
					self.trulyConnectedAfterReceivingResponse = True
				elif readmsg == "0\n":
					send_message_to_ground(json.dumps({"cmd":"status","args":{"arduino":str(str(self.ser.port)+": NOT-shooting")}}))
					self.trulyConnectedAfterReceivingResponse = True
				elif readmsg == "s\n":
					# image taken, save most recent gps into queue
					self.saveGPS()
	                                #time.sleep(.01)
				else:
					print("UNKNOWN MESSAGE FROM ARDUINO "+str(self.ser.port)+": \'"+readmsg+"\'")
				time.sleep(0.001)
						
		self.ispolling = False
	
	def saveGPS(self):
            #if self.images_count >=1:
            #    return
            curtime = time.time()
            location = GPSTelem.connection.ask_gps()
            print("Save GPS(Image Taken): "+str(curtime)+" count: "+str(self.images_count)+" location: "+str(location))
	    self.gps_dict[curtime] = location
            self.images_count+=1
            self.gps_queue.append(location)

