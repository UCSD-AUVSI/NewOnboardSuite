import sys, time
import subprocess, os

def TryCastInt(x):
	try:
		aaaaaa = int(x)
		return True
	except:
		return False

def LaunchServer(argv):
	currfilepath = os.path.dirname(os.path.abspath(__file__))
	path2obcserver = currfilepath+"/../OBC"
	iptolisten = 'x'
	usescurecoms = 0
	with open('server_autostartup_settings.txt') as settingsfile:
		for line in settingsfile:
			if 'ipv4addressforlisten' in line:
				linespl = line.replace('\n',' ').split(' ')
				iptolisten = linespl[2]
				print("will listen at ip \'"+str(iptolisten)+"\'")
			if 'usesecurecomms' in line:
				linespl = line.replace('\n',' ').split(' ')
				maybeusecomms = linespl[2]
				if TryCastInt(maybeusecomms):
					usescurecoms = int(maybeusecomms)
				if usescurecoms != 0:
					print("USING SECURE COMMS")
				else:
					print("WARNING: USING INSECURE COMMS")
	return subprocess.call(["python", "main_server.py", iptolisten, str(usescurecoms)], cwd=path2obcserver)

def ContinuouslyCheckServer(argv):
	while True:
		print("(re)starting...")
		try:
			print("######################################################################### launching OBC python server")
			LaunchServer(argv)
			time.sleep(999000000) #31 years
		except:
			print("OBC python server crash? "+str(sys.exc_info()[0]))
			time.sleep(1)

#-----------------------------------------------------------
# execute main()... this needs to be at the end
#
if __name__ == "__main__":
	ContinuouslyCheckServer(sys.argv[1:])
