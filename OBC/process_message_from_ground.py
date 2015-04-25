
import json
import os
from serial_to_Arduino import globalvar_connection as ArduinoUSBconn

#-----------------------------------------------------------
#
def callback(data):
	print "received message from ground station: \"" + str(data) + "\""
	
	# this needs to be a common interface between all UCSD AUVSI software parts: MissionDirector, Heimdall, NewOnboardSuite, etc.
	json_data = json.loads(data)
	command = json_data["command"]
	args = json_data["args"]
	
	print("command == "+str(command)+", args == "+str(args))
	
	if command == "imaging":
		print("COMMAND WAS IMAGING")
		if args["do"] == "start":
			ArduinoUSBconn.connection.write("1\n")
		if args["do"] == "stop":
			ArduinoUSBconn.connection.write("0\n")
	
	if command == "sric-connect":
		ip_address = args["ip"]
		subnet = args["subnet"]
		folder = args["folder"]
		username = args["username"]
		password = args["password"]
		
		login_credentials = False
		while(not login_credentials):
			# run script 
			login_credentials=True
	
	if command == "sric-upload":
		# try and upload image to team folder
		path = args["folder"]
		
		uploaded = False
		while(not uploaded):
			#try and upload the image at that path
			uploaded=True



