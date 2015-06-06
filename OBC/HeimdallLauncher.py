import os, time, threading


def LaunchServer____private():
	os.system("(cd /home/auvsi/AUVSI/Heimdall/build && ./bin/HServer)")


def LaunchClient____private():
	os.system("(cd /home/auvsi/AUVSI/Heimdall/build && ./bin/HClient --stubs --images FOLDER_WATCH [--folder\ /home/auvsi/AUVSI/NewOnboardSuite/GeotaggedImagesFromCamera] --saliency SPECTRAL_SALIENCY --verif PLANE_VERIF)")


def Launch():
	thread = threading.Thread(target=LaunchServer____private)
	thread.daemon = True
	thread.start()
	time.sleep(0.1)
	thread2 = threading.Thread(target=LaunchClient____private)
	thread2.daemon = True
	thread2.start()
