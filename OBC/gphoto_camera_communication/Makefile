CFLAGS = 
CXXFLAGS = -I/usr/include/python2.7 -fPIC


LIBS = -lpthread -lgphoto2 -lpython2.7 -lboost_python-py27
LINKFLAGS = -shared -Wl,--export-dynamic
HEADERS = CameraControl.h ImageSync.h SharedInfo.h
OBJ = BoostPythonCPP.o CameraControl.o ImageSync.o SharedInfo.o

LINK_TARGET = pytogphotocpplib.so
REBUILDABLES = $(OBJ) $(LINK_TARGET)

all: $(LINK_TARGET)
	echo All done

clean:
	rm -f $(REBUILDABLES)
	echo Clean done

cleanobjs:
	rm -f $(OBJ)
	echo Cleaned object files

$(LINK_TARGET): $(OBJ)
	$(CXX) $(LINKFLAGS) $(LIBS) -o $@ $^
	rm -f $(OBJ)
	echo Done

%.o: %.cpp
	$(CXX) -c $(CXXFLAGS) $<

