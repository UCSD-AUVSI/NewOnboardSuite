#ifndef __SHAREDINFOH__
#define __SHAREDINFOH__

int initCamera();
Camera* getMyCamera();
GPContext* getMyContext();
int setTTYPorts(char* TLM);
char* getTLMTTY();

#endif