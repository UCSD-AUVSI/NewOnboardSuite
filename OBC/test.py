import sys
from networking_to_ground import server_multiport
from networking_to_ground import ports
import process_message_from_ground
from serial_to_Arduino import globalvar_connection as ArduinoUSBconn
import gphoto_camera_communication
from telem_listener import globalvar_connection_gps_telem as GPSTelem
from telem_listener import globalvar_connection_exif_data as ExifData
import time



# create gps listener which listens for gps coordinates from whatever
print GPSTelem.connection
GPSTelem.connection.threadedconnect()

# create folder watch that adds exif data to images
ExifData.connection.threadedconnect()
print "Hello"
while True:
    time.sleep(1)
