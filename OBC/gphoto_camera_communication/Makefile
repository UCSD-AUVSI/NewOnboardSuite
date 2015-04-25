CFLAGS = 
CXXFLAGS = -I/usr/include/python2.7 -fPIC -std=c++11


LIBS = -lpthread -lgphoto2 -lboost_python-py27 -lpython2.7
LINKFLAGS = -shared -Wl,--export-dynamic,-soname,
HEADERS = CameraControl.h ImageSync.h SharedInfo.h
OBJ = BoostPythonCPP.o CameraControl.o ImageSync.o SharedInfo.o

LINK_TARGET = pytogphotocpplib.so
REBUILDABLES = $(OBJ) $(LINK_TARGET)

all: $(LINK_TARGET)
	echo All done

clean:
	rm -f $(REBUILDABLES)
	rm -f *.pyc
	echo Clean done

cleanobjs:
	rm -f $(OBJ)
	echo Cleaned object files

$(LINK_TARGET): $(OBJ)
	$(CXX) $(LINKFLAGS)$(LINK_TARGET) -o $@ $^ $(LIBS)
	rm -f $(OBJ)
	echo Done

%.o: %.cpp
	$(CXX) -c $(CXXFLAGS) $<

