import os, time, threading, subprocess, json
from networking_to_ground.send_message_to_ground import send_message_to_ground

class HeimdallLauncher(object):
	def __init__(self):
		self.serverHasBeenLaunched = (False, '')
		self.clientHasBeenLaunched = (False, '')
		
		self.currfilepath = os.path.dirname(os.path.abspath(__file__)) #points to NewOnboardSuite/OBC where HeimdallLauncher.py is
		self.imagespath = self.currfilepath+"/../GeotaggedImagesFromCamera"
		self.heimdallrunpath = self.currfilepath+"/../../Heimdall/build"
		self.heimdallclientargs = ['--stubs','--images','FOLDER_WATCH_2015','[--folder '+self.imagespath+']','--saliency','SPECTRAL_SALIENCY','--verif','PLANE_VERIF']
	
	
	def LaunchHeimallProg(self, runcmd, isClient):
		try:
			hprocess = subprocess.Popen(runcmd, cwd=self.heimdallrunpath)#, stdout=STDOUT, stderr=STDERR)
			time.sleep(0.5)
			outcheck = hprocess.poll()
			if outcheck is None: #it hasn't shut down yet! it's still running
				if isClient:
					self.clientHasBeenLaunched = (True, hprocess)
				else:
					self.serverHasBeenLaunched = (True, hprocess)
				if self.serverHasBeenLaunched[0] == True and self.clientHasBeenLaunched[0] == True:
					print("Heimdall client and server both launched successfully")
					send_message_to_ground(json.dumps({"cmd":"status","args":{"OBC-Heimdall":"launched successfully"}}))
				else:
					if isClient:
						print("Heimdall client launched successfully")
					else:
						print("Heimdall server launched successfully")
			else:
				send_message_to_ground(json.dumps({"cmd":"status","args":{"OBC-Heimdall":"client","returned":str(outcheck)}}))
		except Exception, e:
			if isClient:
				print("Exception running Heimdall client: "+str(e))
				send_message_to_ground(json.dumps({"cmd":"status","args":{"OBC-Heimdall":"client","error":str(e)}}))
			else:
				print("Exception running Heimdall server: "+str(e))
				send_message_to_ground(json.dumps({"cmd":"status","args":{"OBC-Heimdall":"server","error":str(e)}}))
	
	def LaunchServer____private(self):
		print("Launching Heimdall server")
		runcmd = [self.heimdallrunpath+'/bin/HServer']
		self.LaunchHeimallProg(runcmd, False)
	
	def LaunchClient____private(self):
		print("Launching Heimdall client: "+str(self.heimdallclientargs))
		runcmd = [self.heimdallrunpath+'/bin/HClient']
		runcmd.extend(self.heimdallclientargs)
		self.LaunchHeimallProg(runcmd, True)
	
	def CheckStatus(self):
		def genretmsg(prefix, clBool, svBool):
			if clBool == False and svBool == False:
				return(prefix+"Neither server nor client running")
			elif clBool == True and svBool == False:
				return(prefix+"Client running but server stopped")
			elif clBool == False and svBool == True:
				return(prefix+"Server running but client stopped")
			else:
				return(prefix+"Both client and server are running")
		if self.clientHasBeenLaunched[0] == True and self.serverHasBeenLaunched[0] == True:
			clBool = (self.clientHasBeenLaunched[1].poll() is None)
			svBool = (self.serverHasBeenLaunched[1].poll() is None)
			return genretmsg("good?: ", clBool, svBool)
		return genretmsg("probably stopped?: ", self.clientHasBeenLaunched[0], self.serverHasBeenLaunched[0])
	
	def KillHeimdall(self):
		if self.serverHasBeenLaunched[0] == True:
			self.serverHasBeenLaunched[1].kill() #terminate() and wait() is more polite like a Ctrl+C
		if self.clientHasBeenLaunched[0] == True:
			self.serverHasBeenLaunched[1].kill() #terminate() and wait() is more polite like a Ctrl+C
		self.serverHasBeenLaunched = (False, '')
		self.clientHasBeenLaunched = (False, '')
		send_message_to_ground(json.dumps({"cmd":"status","args":{"OBC-Heimdall":"killed"}}))
	
	def Launch(self):
		print("Launching Heimdall")
		self.LaunchServer____private()
		self.LaunchClient____private()
		'''thread = threading.Thread(target=self.LaunchServer____private)
		thread.daemon = True
		thread.start()
		time.sleep(0.1)
		thread2 = threading.Thread(target=self.LaunchClient____private)
		thread2.daemon = True
		thread2.start()'''

heimdallLauncherInstance = HeimdallLauncher()
