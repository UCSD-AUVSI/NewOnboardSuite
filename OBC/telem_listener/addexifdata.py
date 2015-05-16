from serial_to_Arduino import globalvar_connection as ArduinoUSBconn
import os
import threading
import piexif
from PIL import Image
import time

FOLDER = "../ImagesFromCamera"
OUTPUTFOLDER = "../GeotaggedImagesFromCamera"
HARD_CODE_RELATIVE = 20
class AddExifData(object):

    def __init__(self):
	current_files = os.listdir(FOLDER)
	sanitized_files = []
        for file in current_files:
            if file[-4:] == ".jpg":
                sanitized_files.append(file)
        self.files = sanitized_files
        self.folder_lock = threading.Lock()
        self.listener_started = False

    def threadedconnect(self):
        if self.listener_started == False:
            self.listener_started = True
            self.mythread = threading.Thread(target=self.continous_watch)
            self.mythread.daemon = True
            self.mythread.start()

    def add_exif_data(self, filename):
        # pop top gps coordinate from queue
        location = ArduinoUSBconn.connection.gps_queue.popleft()

        absolute_alt = location["alt"]
        relative_alt = location["rel_alt"]
        lat = location["lat"]
        long = location["lng"]
        heading = location["heading"]
        calc_ground = absolute_alt - relative_alt
	
	print("add_exif_data() called on file \""+filename+"\", found latitude "+str(lat)+" and longitude "+str(long))
	
        im = Image.open(FOLDER+"/"+filename)
        exif_dict = piexif.load(im.info["exif"])
        exif_dict["GPS"][piexif.GPSIFD.GPSSpeed] = (int(round(calc_ground*100)), 100)
        exif_dict["GPS"][piexif.GPSIFD.GPSAltitude] = (int(round(absolute_alt*100)), 100)
        exif_dict["GPS"][piexif.GPSIFD.GPSImgDirection] = (int(round(heading*1000)), 1000)
        exif_dict["GPS"][piexif.GPSIFD.GPSLongitude] = ((int(round(long*1000000)), 1000000))
        exif_dict["GPS"][piexif.GPSIFD.GPSLatitude] = ((int(round(lat*1000000)), 100000))
        exif_dict["GPS"][piexif.GPSIFD.GPSTrack] = ((int(round(relative_alt*100)), 100))
        exif_bytes = piexif.dump(exif_dict)
        im.save(OUTPUTFOLDER+"/"+filename, "jpeg", exif=exif_bytes, quality=90)

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
            if file[-4:] == ".jpg":
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
