import sys
sys.path.append("../pymavlink" )
sys.path.append("pymavlink")
import time
import threading
import mavutil
from mavlink import *

class GPSTelemListener(object):

    def __init__(self):
        self.current = {"lat":0,"lng":0, "alt":0, "rel_alt":0, "heading":0}
        self.lock = threading.Lock()
        self.listener_started = False
    def run_location(self):
        #self.conn = mavutil.mavlink_connection("/dev/ttyUSB0", baud=57600)   #tcp:127.0.0.1:9000")
        print "Set CALLBACK"
        #self.conn.mav.set_callback(self.get_gps_callback)
        print "Getting mavlink Connection:"
        while True:
            #location = self.conn.location()
            location = mavutil.location(37.235,39.323,400,20, 90)
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
