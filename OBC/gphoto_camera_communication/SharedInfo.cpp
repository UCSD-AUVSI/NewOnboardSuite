#include "SharedInfo.h"
#include <stdio.h>
#include <string.h>

/*extern*/ std::string ImagesFolder = std::string();

Camera* my_Camera; 
GPContext* my_Context;
char TLMTTY[15];

int initCamera(){
    gp_camera_new(&my_Camera);
    my_Context = gp_context_new();

    int result = gp_camera_init(my_Camera, my_Context);
    printf(" Camera Init Result: %d ", result);

    if(result == -105){
        printf(" Camera not found, quitting. ");
        return -105;
    }
    printf(" camera successfully found!\n");	

    return 0;
}

Camera* getMyCamera(){
    return my_Camera;
}

GPContext* getMyContext(){
    return my_Context;
}

int setTTYPorts(char* TLM){
    strncpy(TLMTTY, TLM, 15);
    return 0;
}

char* getTLMTTY()   {
    return TLMTTY;
}
