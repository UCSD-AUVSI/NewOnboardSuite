#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <iostream>
#include "SharedInit.h"

int main(int argc, char ** argv) {
	if(argc <= 1) {
		printf("Usage:  {ImagesFolder}\n");
		return -1;
	}
	return doInitCameraListeners(argv[1]);
}

