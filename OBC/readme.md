Arduino code triggers image capture;
gphoto pulls image files (JPEGs) off of the camera's sd card as they are taken
JPEGs are saved in the folder "ImagesFromCamera"
todo: synchronize GPS telemetry with those JPEGs

requirements to run this:
sudo pip install pyserial

need to cd into "gphoto_camera_communication" and make (run command "make")
since the C/C++ code needs to be compiled


