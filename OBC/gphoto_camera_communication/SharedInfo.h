#ifndef __SHAREDINFOH__
#define __SHAREDINFOH__

#include <gphoto2/gphoto2.h>
#include <string>

int initCamera();
Camera* getMyCamera();
GPContext* getMyContext();
int setTTYPorts(char* TLM);
char* getTLMTTY();

extern std::string ImagesFolder;

#endif