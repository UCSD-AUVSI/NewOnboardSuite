CFLAGS = 
CXXFLAGS = -I/usr/include/python2.7 -fPIC -std=c++11

###LIBLIBS = -lpthread -lgphoto2 -lboost_python-py27 -lpython2.7
###LIBLINKFLAGS = -shared -Wl,--export-dynamic,-soname,
EXECLIBS = -lpthread -lgphoto2
HEADERS = CameraControl.h ImageSync.h SharedInfo.h SharedInit.h
OBJSHARE = CameraControl.o ImageSync.o SharedInfo.o SharedInit.o
###OBJLIB = BoostPythonCPP.o
OBJEXEC = StartListenersMainExec.o

EXEC_TARGET = gphotocppexec
###LIB_TARGET = pytogphotocpplib.so
OBJALL = $(OBJSHARE) $(OBJEXEC) ###$(OBJLIB)
REBUILDABLES = $(OBJALL) $(EXEC_TARGET) ###$(LIB_TARGET)

all: $(EXEC_TARGET) ###$(LIB_TARGET)
	echo All done

clean:
	rm -f $(REBUILDABLES)
	rm -f *.pyc
	echo Clean done

cleanobj:
	rm -f $(OBJALL)
	rm -f *.pyc
	echo Cleaned object files
cleanobjs:
	rm -f $(OBJALL)
	rm -f *.pyc
	echo Cleaned object files

$(EXEC_TARGET): $(OBJSHARE) $(OBJEXEC)
	$(CXX) -o $@ $^ $(EXECLIBS)
	echo Done

###$(LIB_TARGET): $(OBJSHARE) $(OBJLIB)
###	$(CXX) $(LIBLINKFLAGS)$(LIB_TARGET) -o $@ $^ $(LIBLIBS)
###	echo Done

%.o: %.cpp
	$(CXX) -c $(CXXFLAGS) $<

