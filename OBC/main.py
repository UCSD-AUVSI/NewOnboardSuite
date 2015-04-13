import sys
from networking_to_ground import server_multiport
from networking_to_ground import ports
import process_message_from_ground


#-----------------------------------------------------------
# main(): setup and start listen server
#
def main(argv):
	
	# Setup several parallel listeners
	ports_and_callbacks = []
	ports_and_callbacks.append((ports.listenport_from_ground, process_message_from_ground.callback))
	
	# Start server and wait here for keyboard interrupt
	s = server_multiport.server()
	s.start(ports_and_callbacks, True)


#-----------------------------------------------------------
# execute main()... this needs to be at the end
#
if __name__ == "__main__":
	main(sys.argv[1:])







