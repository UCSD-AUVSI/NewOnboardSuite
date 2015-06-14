import os, time, threading


def LaunchServer____private():
	print("Launching Heimdall server: (cd /home/auvsi/AUVSI/Heimdall/build && ./bin/HServer)")
	os.system("(cd /home/auvsi/AUVSI/Heimdall/build && ./bin/HServer)")


def LaunchClient____private():
	print("Launching Heimdall client: (cd /home/auvsi/AUVSI/Heimdall/build && ./bin/HClient --stubs --images FOLDER_WATCH_2015 [--folder\ /home/auvsi/AUVSI/NewOnboardSuite/GeotaggedImagesFromCamera] --saliency SPECTRAL_SALIENCY --verif PLANE_VERIF)")
	os.system("(cd /home/auvsi/AUVSI/Heimdall/build && ./bin/HClient --stubs --images FOLDER_WATCH_2015 [--folder\ /home/auvsi/AUVSI/NewOnboardSuite/GeotaggedImagesFromCamera] --saliency SPECTRAL_SALIENCY --verif PLANE_VERIF)")


def Launch():
	print "Launch Heimdall"
        thread = threading.Thread(target=LaunchServer____private)
	thread.daemon = True
	thread.start()
	time.sleep(0.1)
	thread2 = threading.Thread(target=LaunchClient____private)
	thread2.daemon = True
	thread2.start()
