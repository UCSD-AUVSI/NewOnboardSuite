import sys
sys.path.append("../pymavlink" )
sys.path.append("pymavlink")
import time
import threading
import mavutil
from mavlink import *
import serial  #used to catch exception when USB serial is not plugged in
import serial_to_Arduino

class GPSTelemListener(object):

    def __init__(self):
        self.current = {"lat":0,"lng":0, "alt":0, "rel_alt":0, "heading":0}
        self.lock = threading.Lock()
        self.listener_started = False
        self.serport = "/dev/ttyUSB0"
	self.possibleSerPortIdxCheck = 0
	self.possibleSerPorts = ["/dev/ttyUSB0", "/dev/ttyUSB1", "/dev/ttyUSB2", "/dev/ttyUSB3", "/dev/ttyACM0", "/dev/ttyACM1", "/dev/ttyACM2", "/dev/ttyACM3"]
	self.ispluggedinlocker = threading.Lock()
	self.is_plugged_in_and_working = False
    
    def GetStatus(self):
        isplugggedin = False
	self.ispluggedinlocker.acquire()
	if self.is_plugged_in_and_working:
            isplugggedin = True
	self.ispluggedinlocker.release()
        if isplugggedin:
		return "Plugged in."
	else:
		return "Not plugged in; checking "+str(self.possibleSerPorts)
    
    def run_location(self):
        while serial_to_Arduino.globalvar_connection.connection.trulyConnectedAfterReceivingResponse == False:
            print("telem is waiting for Arduino to connect before trying to connect")
            time.sleep(1)
        arduinoserport = str(serial_to_Arduino.globalvar_connection.connection.ser.port)
        if arduinoserport in self.possibleSerPorts:
            self.possibleSerPorts.remove(arduinoserport)
        print("Since arduino connected on "+arduinoserport+", will try to connect telem on other ports: "+str(self.possibleSerPorts))
        keeptrying = True
        while keeptrying:
            try:
                self.conn = mavutil.mavlink_connection(self.serport, baud=57600)
                time.sleep(1)
                keeptrying = False
                print("telemetry was plugged into \'"+self.serport+"\'")
            except serial.serialutil.SerialException:
                print("waiting for telemetry USB to be plugged in...")
                time.sleep(1)
                # if we can't find it on USB0, try other USB ports
                self.possibleSerPortIdxCheck += 1
                if self.possibleSerPortIdxCheck == len(self.possibleSerPorts):
                    self.possibleSerPortIdxCheck = 0
                self.serport = self.possibleSerPorts[self.possibleSerPortIdxCheck]
	
	print("Telemetry USB was connected successfully")
	self.ispluggedinlocker.acquire()
	self.is_plugged_in_and_working = True
	self.ispluggedinlocker.release()
	
	print "Set CALLBACK"
	self.conn.mav.set_callback(self.get_gps_callback)
	print "Getting mavlink Connection:"
        while True:
            location = self.conn.location()
            #location = mavutil.location(37.235,39.323,400,20, 90)
            self.lock.acquire()
            self.current = {"lat":location.lat,"lng":location.lng, "alt":location.alt, "rel_alt":location.rel_alt, "heading":location.heading}
            self.lock.release()
            time.sleep(0.01)

    def ask_gps(self):
        self.lock.acquire()
        location = self.current
        self.lock.release()
        return location

    def threadedconnect(self):
        if self.listener_started == False:
            self.listener_started = True
            self.mythread = threading.Thread(target=self.run_location)
            self.mythread.daemon = True
            self.mythread.start()

    def get_gps_callback(self, m):
	print "Callback"
	print m
        mtype = m.get_type()
	print mtype
