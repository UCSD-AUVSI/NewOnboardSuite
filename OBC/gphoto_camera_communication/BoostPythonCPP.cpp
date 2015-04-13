#include <iostream>
#include <stdint.h>
#include <opencv2/imgproc/imgproc.hpp>
#include <boost/python.hpp>
#include "SharedUtils/PythonUtils.hpp"
namespace bp = boost::python;
using std::cout; using std::endl;

bp::object donothing(double timestamp, double latitude, double longitude)
{
	return bp::string("hello");
}

static void init()
{
    Py_Initialize();
    import_array();
}

BOOST_PYTHON_MODULE(pytogphotocpplib)
{
    init();
    bp::def("donothing", donothing);
}
