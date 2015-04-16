import sys
from networking_to_ground import server_multiport
from networking_to_ground import ports
import process_message_from_ground


#-----------------------------------------------------------
# main(): setup and start listen server
#
def main(argv):
	if len(sys.argv) <= 1:
		print("args:   [ipv4address for listen; can be localhost]")
		quit()
	
	ipv4address = str(sys.argv[1])
	print("will listen at IP "+ipv4address)
	
	# Setup listen server to listen to ground station
	ports_and_callbacks = []
	ports_and_callbacks.append((ports.listenport_from_ground, process_message_from_ground.callback))
	
	# Start server and wait here for keyboard interrupt
	s = server_multiport.server()
	s.start(ports_and_callbacks, ipv4address, True)


#-----------------------------------------------------------
# execute main()... this needs to be at the end
#
if __name__ == "__main__":
	main(sys.argv[1:])







