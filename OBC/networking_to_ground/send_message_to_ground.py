import socket, threading
import ports

def send_message_to_ground(msg):
	
	# Use this to dispatch the message to another thread so the main thread can't freeze
	thread = threading.Thread(target=private___dispatch_msg, args=(msg, ports.outport_to_ground, ports.groundipaddress))
	thread.daemon = True
	thread.start()


#--------------------------------------------------------------------------------------
# Use this to dispatch the message to another thread so the main thread can't freeze
#
def private___dispatch_msg(msg, port, IPaddr):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((IPaddr,port))
	s.send(msg)
	s.close()

