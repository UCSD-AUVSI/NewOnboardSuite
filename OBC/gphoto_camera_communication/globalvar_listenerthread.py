import pytogphotocpplib
import threading

def doStartCameraListeners():
	imagesfolder = "../ImagesFromCamera"
	pytogphotocpplib.initCameraListeners(imagesfolder)
	import time
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
