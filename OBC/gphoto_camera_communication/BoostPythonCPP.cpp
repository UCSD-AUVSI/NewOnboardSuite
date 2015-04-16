#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <pthread.h>
#include <gphoto2/gphoto2.h>
#include <iostream>
#include <stdint.h>

#include "ImageSync.h"
#include "SharedInfo.h"

#include <boost/python.hpp>
namespace bp = boost::python;
using std::cout; using std::endl;


bp::object sayhello(double timestamp, double latitude, double longitude)
{
	cout<<"hello"<<endl;
	return bp::str("hello");
}


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
int initSuite() {
	initImageSync();
	printf("Initialized Listeners/Syncs\n");
	return 0;
}
bp::object initCameraListeners() {
	//Initialize all sub classes
	initSuite();

	//Spawning the three worker threads
	pthread_t getThread, saveThread;

	pthread_create(&getThread, NULL, GetEvents, NULL);
	printf("Started Get Thread\n");
	pthread_create(&saveThread, NULL, SaveFiles, NULL);
	printf("Started Save Thread\n");

	pthread_join(getThread, NULL);
	pthread_join(saveThread, NULL);

	return bp::str("threads exited");
}

static void init()
{
    Py_Initialize();
}

BOOST_PYTHON_MODULE(pytogphotocpplib)
{
    init();
    bp::def("sayhello", sayhello);
    bp::def("initCameraListeners", initCameraListeners);
}







