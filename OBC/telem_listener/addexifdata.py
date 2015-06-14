from serial_to_Arduino import globalvar_connection as ArduinoUSBconn
import os
import threading
import piexif
from PIL import Image
import time
import datetime
from datetime import datetime

FOLDER = "../ImagesFromCamera"
OUTPUTFOLDER = "../GeotaggedImagesFromCamera"
HARD_CODE_RELATIVE = 20
class AddExifData(object):

    def __init__(self):
	current_files = os.listdir(FOLDER)
	sanitized_files = []
        for file in current_files:
            if file[-4:].lower() == ".jpg":
                sanitized_files.append(file)
        self.files = sanitized_files
        self.folder_lock = threading.Lock()
        self.listener_started = False
        self.adds = 0

    def threadedconnect(self):
        if self.listener_started == False:
            self.listener_started = True
            self.mythread = threading.Thread(target=self.continous_watch)
            self.mythread.daemon = True
            self.mythread.start()

    def add_exif_data(self, filename):
        print "----------------------------------------------------------------------------"
        # pop top gps coordinate from queue
        try:
            print "Size of Queue: "+ str(len( ArduinoUSBconn.connection.gps_queue))
            print  ArduinoUSBconn.connection.gps_queue
            location = ArduinoUSBconn.connection.gps_queue.popleft()
        except Exception as e:
            print "Queue is empty"
            print e
            return

        try:
            im = Image.open(FOLDER+"/"+filename)
            exif_dict = piexif.load(im.info["exif"])
            print "AddExif: "+ filename
        except Exception as e:
            print "Couldn't open file "+filename
            print "Error: "+e
            print "----------------------------------------------------------------------------"
            return
        """
        image_time_s = exif_dict["Exif"][piexif.ExifIFD.DateTimeOriginal]
        image_time_ms = int(exif_dict["Exif"][piexif.ExifIFD.SubSecTimeOriginal])
        image_time = time.strptime(image_time_s,"%Y:%m:%d %H:%M:%S")
        image_unix = time.mktime(image_time)
        image_unix = image_unix + image_time_ms/int(len(str(image_time_ms)))
        # copy dict for use in case of modification
        gps_dict = ArduinoUSBconn.connection.gps_dict.copy()
        
        
        if self.adds == 0:
            lowest = 10000000000000000000
            for t in gps_dict:
                if t < lowest:
                    lowest = t
            self.beg_obc_clock = lowest
            self.beg_cam_clock = image_unix
            self.adds = 1

        print gps_dict
        print image_unix 
        # offset camera time to obc time
        image_offset = abs(image_unix - self.beg_cam_clock) 

        closest = 0
        smallest = -1
        for k in gps_dict:
            obc_offset = abs(k - self.beg_obc_clock)
            diff = abs(k - image_unix)
            if smallest == -1:
                if diff < 10:
                    closest = k
                    smallest = diff
            else:
                if diff < smallest and diff < 5:
                    closest = k
                    smallest = diff
        if closest not in gps_dict:
            print "ERROR NO GPS TAG FOR THIS IMAGE" + filename
            print "IMAGE TIME = "+str(image_unix)
            print "----------------------------------------------------------------------------"
            return
        print "Image Time: "+ str(image_unix)
        print "Closest GPS Time: "+ str(closest) + " diff: "+str(smallest)
        print "Location: "+ str(gps_dict[closest])
        #location = gps_dict[closest]
        """ 

        absolute_alt = location["alt"]
        relative_alt = location["rel_alt"]
        calc_ground = abs(absolute_alt - relative_alt)
        lat = location["lat"]
        lon = location["lng"]
        heading = location["heading"]

        # two precision
        absolute_alt = int(round(absolute_alt*100))
        calc_ground = int(round(calc_ground*100))
        relative_alt = int(round(relative_alt*100))

        # three precision
        heading = int(round(heading*1000))
        lat = int(round(abs(lat*1000)))
        lon = int(round(abs(lon*1000)))


        exif_dict["GPS"][piexif.GPSIFD.GPSSpeed] = (calc_ground, 100)
        exif_dict["GPS"][piexif.GPSIFD.GPSAltitude] = (absolute_alt, 100)
        exif_dict["GPS"][piexif.GPSIFD.GPSImgDirection] = (heading, 1000)
        exif_dict["GPS"][piexif.GPSIFD.GPSLongitude] = (lon, 1000)
        exif_dict["GPS"][piexif.GPSIFD.GPSLatitude] = (lat, 1000)
        exif_dict["GPS"][piexif.GPSIFD.GPSTrack] = (relative_alt, 100)
        try:
            exif_bytes = piexif.dump(exif_dict)
            im.save(OUTPUTFOLDER+"/"+filename, "jpeg", exif=exif_bytes, quality=90)
        except Exception as e:
            print "--------"
            print "ERROR Exif data could not be saved"
            print e
            print "Lat "+str(lat)
            print "Long "+str(lon)
            print "Heading "+str(heading)
            print "AAlt "+str(absolute_alt)
            print "RAlt "+str(relative_alt)
            print "CGround "+str(calc_ground)
            print "--------"
        print "exif data added"
        print "----------------------------------------------------------------------------"
    def continous_watch(self):
        while True:
            self.watch_folder()
            time.sleep(0.1)

    def watch_folder(self):
        self.folder_lock.acquire()
        # get all files in the directory
        current_files = os.listdir(FOLDER)

        # remove non jpg files
        sanitized_files = []
        for file in current_files:
            if file[-4:].lower() == ".jpg":
                sanitized_files.append(file)

        # get new files (not in self.files)
        new_files = []
        for file in sanitized_files:
            if file not in self.files:
                new_files.append(file)

        # for the new files add exif data
        for file in new_files:
            self.add_exif_data(file)
        # move sanitized files to files
        self.files = sanitized_files
        self.folder_lock.release()
