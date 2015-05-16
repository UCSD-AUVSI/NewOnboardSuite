import sys
from networking_to_ground import server_multiport
from networking_to_ground import ports
import process_message_from_ground
from serial_to_Arduino import globalvar_connection as ArduinoUSBconn
import gphoto_camera_communication
from telem_listener import globalvar_connection_gps_telem as GPSTelem
from telem_listener import globalvar_connection_exif_data as ExifData


#-----------------------------------------------------------
# main(): setup and start listen server
#
def main(argv):
	if len(argv) < 2:
		print("args:  {ipv4address-for-listen}  {ipv4address-of-ground}")
		quit()
	ipv4address = str(argv[0])
	print("will listen on IP \'"+ipv4address+"\'")

	ports.server_ssl_details = server_multiport.SSLSecurityDetails(True)
	ports.server_ssl_details.cacerts = "/home/auvsi/AUVSI/sslcerts/MDclientJason.crt"
	ports.server_ssl_details.certfile = "/home/auvsi/AUVSI/sslcerts/nobs-auvsi-cert-server.crt"
	ports.server_ssl_details.keyfile = "/home/auvsi/AUVSI/sslcerts/nobs-auvsi-cert-server.key.nopass"

	#ports.groundipaddress = str(argv[1])
	#print("will reach ground station IP at \'"+ports.groundipaddress+"\'")

	# start gphoto listener to camera, which pulls images off the camera
	gphoto_camera_communication.globalvar_listenerthread.globalGPhotoCThread.Start()

	# initiate connection to Arduino, which triggers image capture with the trigger cable
	ArduinoUSBconn.connection.threadedconnect() # connect so serial link can "warm up"

    # create gps listener which listens for gps coordinates from whatever
    GPSTelem.connection.threadedconnect()

	# create folder watch that adds exif data to images
	ExifData.connection.threadedconnect()

	# Setup listen server to listen to ground station
	ports_and_callbacks = []

	ports_and_callbacks.append((ports.port_from_ground, process_message_from_ground.callback, ports.server_ssl_details))

	# Start PlaneOBC listen server and wait here for keyboard interrupt
	ports.global_listenserver = server_multiport.server()
	ports.global_listenserver.start(ports_and_callbacks, ipv4address, True, True)



    #this line should never be reached - Jason 2015 2:26pm May 16
	print("server done?????????????????????????????????????????????????")


#-----------------------------------------------------------
# execute main()... this needs to be at the end
#
if __name__ == "__main__":
	main(sys.argv[1:])
