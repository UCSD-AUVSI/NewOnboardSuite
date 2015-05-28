import subprocess, os
import threading

def doStartCameraListeners():
	imagesfolder = "../../ImagesFromCamera"
	exe2call = "./gphotocppexec"
	currfolderpath = os.path.dirname(os.path.abspath(__file__))
	callresult = subprocess.call([exe2call, imagesfolder], cwd=currfolderpath)
	import time
	while callresult != 0:
		if callresult != -1:
			if callresult == -11:
				print("WARNING: SEGFAULT IN CAMERA CODE")
			else:
				print(" unusual error from camera subprocess: code "+str(callresult))
		print("was the camera not found? waiting for camera to be plugged in...")
		time.sleep(1)
		callresult = subprocess.call([exe2call, imagesfolder], cwd=currfolderpath)
	while True:
		time.sleep(1)

# Use this to dispatch the gphoto camera event listeners to another thread,
# where they will listen until the heat death of the universe (or this program quits)

class GPhotoCThread(object):
	def __init__(self):
		self.started = False
		self.mythread = threading.Thread(target=doStartCameraListeners)
		self.mythread.daemon = True
	def Start(self):
		if self.started == False:
			print("starting GPhotoCThread()")
			self.started = True
			self.mythread.start()

globalGPhotoCThread = GPhotoCThread()
