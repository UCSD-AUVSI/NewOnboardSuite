import socket, threading
import ports
import time
import server_multiport

def send_message_to_ground(msg):
	
	# Use this to dispatch the message to another thread so the main thread can't freeze
	thread = threading.Thread(target=private___dispatch_msg, args=(msg, ports.port_to_ground, ports.groundipaddress))
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
		
		if ports.socket_to_ground_is_opened == False:
			MYCERTFILE = ports.server_ssl_details.certfile
			MYKEYFILE = ports.server_ssl_details.keyfile
			SERVERCERTFILE = ports.server_ssl_details.cacerts
		
			ports.IPaddr_PlaneOBC = IPaddr
			if os.path.isfile(MYCERTFILE) == False:
				print("WARNING: SSL SERVER CA CERT FILE \""+MYCERTFILE+"\" NOT FOUND")
			if os.path.isfile(SERVERCERTFILE) == False:
				print("WARNING: SSL CLIENT CERT FILE \""+SERVERCERTFILE+"\" NOT FOUND")
			s_ = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			ports.secure_socket_to_ground = ssl.wrap_socket(s_,
						ssl_version=ssl.PROTOCOL_TLSv1,
						ca_certs=SERVERCERTFILE,
						cert_reqs=ssl.CERT_REQUIRED,
						certfile=MYCERTFILE,
						keyfile=MYKEYFILE)
			ports.secure_socket_to_ground.connect((IPaddr,port))
			ports.socket_to_ground_is_opened = True
		
		ports.secure_socket_to_ground.send(msg)



