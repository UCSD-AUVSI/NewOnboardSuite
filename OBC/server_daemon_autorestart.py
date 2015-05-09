import sys, time
from main_server import main
from networking_to_ground import server_multiport
from networking_to_ground import ports
import threading

def LaunchServer(argv):
	iptolisten = 'x'
	ipofground = 'x'
	with open('server_autostartup_settings.txt') as settingsfile:
		for line in settingsfile:
			if 'ipv4addressforlisten' in line:
				linespl = line.replace('\n',' ').split(' ')
				iptolisten = linespl[2]
				print("will listen at ip \'"+str(iptolisten)+"\'")
			if 'ipv4addressofground' in line:
				linespl = line.replace('\n',' ').split(' ')
				ipofground = linespl[2]
				print("ground is ip \'"+str(ipofground)+"\'")
	main([iptolisten, ipofground])

def RespondToParentAutorestarter(hbmsg):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect(('localhost',ports.localhost_port_for_auto_server_restart_selfchecks_parent))
	s.send("hi")
	s.close()

def ThreadedLaunchServer(argv):
	thread = threading.Thread(target=LaunchServer, args=(argv,))
	thread.daemon = True
	thread.start()
	time.sleep(1)
	# Setup listen server to listen to parent autorestarter
	ports_and_callbacks = []
	ports_and_callbacks.append((ports.localhost_port_for_auto_server_restart_selfchecks_sub, RespondToParentAutorestarter))
	ss = server_multiport.server()
	ss.start(ports_and_callbacks, 'localhost', True)

def ContinuouslyCheckServer(argv):
	while True:
		print("(re)starting...")
		try:
			ThreadedLaunchServer(argv)
			time.sleep(864000000)
		except:
			print("crash? "+str(sys.exc_info()[0]))
			time.sleep(1)

#-----------------------------------------------------------
# execute main()... this needs to be at the end
#
if __name__ == "__main__":
	ContinuouslyCheckServer(sys.argv[1:])
