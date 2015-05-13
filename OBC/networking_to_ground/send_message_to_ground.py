import socket, threading
import ports
import time
import server_multiport

def send_message_to_ground(msg):
	
	# Use this to dispatch the message to another thread so the main thread can't freeze
	thread = threading.Thread(target=private___dispatch_msg, args=(msg, ports.port_tofrom_ground, ports.groundipaddress))
	thread.daemon = True
	thread.start()


#--------------------------------------------------------------------------------------
# Use this to dispatch the message to another thread so the main thread can't freeze
#
def private___dispatch_msg(msg, port, IPaddr):
	if IPaddr == "localhost" or IPaddr == "127.0.0.1":
		print("FORWARDING MESSAGER TO LOCALHOST GROUND STATION")
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((IPaddr,port))
		s.send(msg)
		s.close()
	else:
		print("FORWARDING MESSAGER TO SSL NONLOCAL GROUND STATION")
		clientsockdeets = ports.global_listenserver.ReplyToSocketOnPort(port, msg)
		if True:
			print("message sent")
		else:
			print("GROUND STATION SOCKET NOT CONNECTED??")
