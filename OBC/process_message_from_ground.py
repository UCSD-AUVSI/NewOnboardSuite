
import json
import os
from serial_to_Arduino import globalvar_connection as ArduinoUSBconn
from networking_to_ground.send_message_to_ground import send_message_to_ground
from networking_to_ground import ports
from telem_listener import globalvar_connection_gps_telem
import OBC_temp_and_CPU_status
import HeimdallLauncher
import gphoto_camera_communication
import traceback

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
			if "cpu-temp" in args:
				try:
					cpumsg = json.dumps(OBC_temp_and_CPU_status.GetCPUTemps())
				except:
					cpumsg = "Exception in OBC temp status"
				statusargs["cpu-temp"] = cpumsg
			if "cpu-freq" in args:
				try:
					cpumsg = json.dumps(OBC_temp_and_CPU_status.GetCPUfrequencySettings())
				except:
					cpumsg = "Exception in OBC freq status"
				statusargs["cpu-freq"] = cpumsg
			if "telem" in args:
				statusargs["telem"] = globalvar_connection_gps_telem.connection.GetStatus()
			if "DSLR" in args:
				statusargs["DSLR"] = gphoto_camera_communication.globalvar_listenerthread.globalGPhotoCThread.CheckIfExists()
			if "OBC-Heimdall" in args:
				statusargs["OBC-Heimdall"] = "todo"
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
			HeimdallLauncher.heimdallLauncherInstance.Launch()
			#send_message_to_ground(json.dumps({"cmd":"status","args":{"OBC-Heimdall":"told to launch"}}))
		if cmd == "kill-heimdall":
			print("ground said KILL heimdall")
			HeimdallLauncher.heimdallLauncherInstance.KillHeimdall()
			#send_message_to_ground(json.dumps({"cmd":"status","args":{"OBC-Heimdall":"told to KILL"}}))
		
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
	except Exception, e:
		send_message_to_ground(json.dumps({"cmd":"status","args":{"on-cmd":str(cmd),"error":str(e)}}))
		print("Error processing message from ground: "+str(e))
		traceback.print_exc()



