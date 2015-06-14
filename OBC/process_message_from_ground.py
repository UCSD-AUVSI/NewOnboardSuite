
import json
import os
from serial_to_Arduino import globalvar_connection as ArduinoUSBconn
from networking_to_ground.send_message_to_ground import send_message_to_ground
from networking_to_ground import ports
import OBC_temp_and_CPU_status
import HeimdallLauncher

#-----------------------------------------------------------
#
def callback(data, addrinfo):
	try:
		print("callback -- addrinfo -- "+str(addrinfo))
		ports.groundipaddress = addrinfo[0]
		
		print("received message from ground station: \"" + str(data) + "\" of type "+str(type(data)))
		
		# this needs to be a common interface between all UCSD AUVSI software parts: MissionDirector, Heimdall, NewOnboardSuite, etc.
		json_data = json.loads(data)
		print("json message from ground station: \"" + str(json_data) + "\"")
		
		cmd = json_data["cmd"]
		args = json_data["args"]
		
		if cmd == "status":
			statusargs = {}
			if "hello" in args:
				statusargs["hello"] = "reply"
			if "arduino" in args:
				statusargs["arduino"] = ArduinoUSBconn.connection.CheckWriteability()
			if "cpu" in args:
				cpumsg = ""
				try:
					temps = OBC_temp_and_CPU_status.GetCPUTemps()
					freqsinfo = OBC_temp_and_CPU_status.GetCPUfrequencySettings()
					cpumsg = json.dumps((temps,freqsinfo))
				except:
					cpumsg = "Exception in OBC_temp_and_CPU_status"
				statusargs["cpu"] = cpumsg
			if len(statusargs) > 0:
				send_message_to_ground(json.dumps({"cmd":"status","args":statusargs}))
		
		if cmd == "imaging":
			print("COMMAND WAS IMAGING, ARGS WERE "+str(args))
			if "start" in args:
				if ArduinoUSBconn.connection.write("1\n"):
					send_message_to_ground(json.dumps({"cmd":"status","args":{"arduino":"imaging STARTED"}}))
				else:
					send_message_to_ground(json.dumps({"cmd":"status","args":{"arduino":"failed to start imaging"}}))
			if "stop" in args:
				if ArduinoUSBconn.connection.write("0\n"):
					send_message_to_ground(json.dumps({"cmd":"status","args":{"arduino":"imaging STOPPED"}}))
				else:
					send_message_to_ground(json.dumps({"cmd":"status","args":{"arduino":"failed to stop imaging"}}))
		
		if cmd == "start-heimdall":
			print("ground said launch heimdall")
			HeimdallLauncher.Launch()
			send_message_to_ground(json.dumps({"cmd":"status","args":{"heimdall":"heimdall STARTED"}}))
		
		if cmd == "sric-connect":
			ip_address = args["ip"]
			subnet = args["subnet"]
			folder = args["folder"]
			username = args["username"]
			password = args["password"]
		
			login_credentials = False
			while(not login_credentials):
				# run script 
				login_credentials=True
		
		if cmd == "sric-upload":
			# try and upload image to team folder
			path = args["folder"]
		
			uploaded = False
			while(not uploaded):
				#try and upload the image at that path
				uploaded=True
	except:
		print("Error processing message from ground")



