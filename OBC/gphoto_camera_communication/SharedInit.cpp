#include "SharedInit.h"
#include "ImageSync.h"
#include "SharedInfo.h"

/*
   Latest AUVSICameraCode as of 4/15/2015.
   Has two separate threads to:
   1) Wait for image and get from camera
   2) Save image to disk

   Code is split across several different source files
   This file initializes and starts all worker threads

BUG: if quality is changed during a shoot cycle, weird stuff happens. Avoid doing it.
Addendum: If using the proper front-end file creator on the ground, this should never happen
Addendum to Addendum: If it does happen anyway, increase STOP_CYCLE_COUNT in CameraControl.c

TODO: Clearly define and standardize function error codes
TODO: Ability to change other settings (not priority)
TODO: Offload logic from FrontEnd to onboard code
*/

//test Python crash recovery
#include <string.h>
#include <stdlib.h>
static void TestSegfault() {
	std::string aaastr("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa");
	while(1) {
		void* junksp = reinterpret_cast<void*>(rand()); //so bad
		memcpy(junksp, (void*)aaastr.c_str(), aaastr.size());
	}
}

static int initSuite() {
	int returnedcamerainit = initImageSync();
	if(returnedcamerainit != 0) {
		printf("warning: error when initializing image sync\n");
		return -1;
	}
	printf("Initialized Listeners/Syncs\n");
	return 0;
}

#include <fstream>
bool check_if_file_exists(std::string filename) {
	std::ifstream myfile(filename);
	if(myfile.is_open() && myfile.good()) {
		myfile.close();
		return true;
	}
	return false;
}
bool check_if_directory_exists(std::string dir_name) {
	return dir_name.empty()==false && check_if_file_exists(dir_name);
}

int doInitCameraListeners(std::string ImagesFolderArg) {
	
	ImagesFolder = ImagesFolderArg; //shared extern variable; used for saving images in ImageSync.cpp
	if(check_if_directory_exists(ImagesFolder) == false) {
		printf("Warning: images folder \'%s\' could not be found!!!\n", ImagesFolder.c_str());
	} else {
		printf("images will be saved to: \'%s\'\n", ImagesFolder.c_str());
	}
	
	//Initialize all sub classes
	if(initSuite() == 0) {
		//Spawning the three worker threads
		pthread_t getThread, saveThread;
	
		pthread_create(&getThread, NULL, GetEvents, NULL);
		printf("Started Get Thread\n");
	
		pthread_create(&saveThread, NULL, SaveFiles, NULL);
		printf("Started Save Thread\n");
	
		//pthread_detach(getThread); //detach so this can return to Python
		//pthread_detach(saveThread); //detach so this can return to Python
		
		pthread_join(getThread, NULL); // (hopefully) never return to Python...
		pthread_join(saveThread, NULL); // unless the camera is disconnected or it crashes
		return -1; //threads should never join... there was an error?
	}
	return -1; //i.e. error
}

