# NewOnboardSuite
All onboard payload software: OBC + Arduino code for 2015 imaging and telemetry synchronization.

## How to get the OBC code up and running:

In the `OBC` folder, the C/C++ code in `gphoto_camera_communication` needs to be compiled using `make`.

Follow the readme in `ServerSetupScript` so that the onboard Python server will be always on, every time the OBC is booted.

## How to get Arduino imaging running:
Simply use the Arduino IDE to upload the Arduino.ino script to the Arduino device. It can be tested using the script `test_arduino_usb.py` in the folder `OBC/serial_to_Arduino`, which requires the pyserial library to be installed.

## Additional Notes
Images to be used for Heimdall will be saved in GeotaggedImagesFromCamera, where they should have the proper EXIF data for georeferencing.
