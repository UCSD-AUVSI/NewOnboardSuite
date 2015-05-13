import sys
from networking_to_ground import server_multiport
from networking_to_ground import ports
import process_message_from_ground
from serial_to_Arduino import globalvar_connection as ArduinoUSBconn
import gphoto_camera_communication


#-----------------------------------------------------------
# main(): setup and start listen server
#
def main(argv):
	if len(argv) < 2:
		print("args:  {ipv4address-for-listen}  {ipv4address-of-ground}")
		quit()
	ipv4address = str(argv[0])
	print("will listen on IP \'"+ipv4address+"\'")
	
	ssl_details = server_multiport.SSLSecurityDetails(True)
	ssl_details.cacerts = "/home/auvsi/AUVSI/sslcerts/MDclientJason.crt"
	ssl_details.certfile = "/home/auvsi/AUVSI/sslcerts/nobs-auvsi-cert-server.crt"
	ssl_details.keyfile = "/home/auvsi/AUVSI/sslcerts/nobs-auvsi-cert-server.key.nopass"
	
	#ports.groundipaddress = str(argv[1])
	#print("will reach ground station IP at \'"+ports.groundipaddress+"\'")
	
	# start gphoto listener to camera, which pulls images off the camera
	gphoto_camera_communication.globalvar_listenerthread.globalGPhotoCThread.Start()
	
	# initiate connection to Arduino, which triggers image capture with the trigger cable
	ArduinoUSBconn.connection.threadedconnect() # connect so serial link can "warm up"
	
	# Setup listen server to listen to ground station
	ports_and_callbacks = []
	ports_and_callbacks.append((ports.port_tofrom_ground, process_message_from_ground.callback, ssl_details))
	
	# Start PlaneOBC listen server and wait here for keyboard interrupt
	ports.global_listenserver = server_multiport.server()
	ports.global_listenserver.start(ports_and_callbacks, ipv4address, True, True)
	
	print("server done?????????????????????????????????????????????????")


#-----------------------------------------------------------
# execute main()... this needs to be at the end
#
if __name__ == "__main__":
	main(sys.argv[1:])







