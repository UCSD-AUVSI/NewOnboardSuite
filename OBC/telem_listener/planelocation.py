import sys
sys.path.append("../pymavlink" )
sys.path.append("pymavlink")
import time
import threading
import mavutil
from mavlink import *

class GPSTelemListener(object):

    def __init__(self):
        self.current = (0, 0, 0, 0, 0)
        self.lock = threading.Lock()
        self.listener_started = False
    def run_location(self):
        #self.conn = mavutil.mavlink_connection("tcp:127.0.0.1:9000")
        print "Getting mavlink Connection:"
        while True:
            #location = connection.location()
            location = mavutil.location(37.235,39.323,400,20, 90)
            self.lock.acquire()
            self.current = {"lat":location.lat,"lng":location.lng, "alt":location.alt, "rel_alt":location.rel_alt, "heading":location.heading}
            self.lock.release()
            time.sleep(50)

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

    def get_gps_callback(m, connection):
        mtype = m.get_type()
        print "Recieved data of type "+ mtype
        mtype = m.get_type()
        if mtype == "GLOBAL_POSITION_INT":
            print m.lat
            print m.lon
