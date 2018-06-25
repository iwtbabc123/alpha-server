#include "worker_thread.h"
#include "timer.h"
#include "logger.h"

static PyObject*
OnClient(PyObject* self, PyObject* args){
	LogDebug("py->cpp OnClient");

	int sockfd;
	int type;
	char* str;
	int size;
	if (!PyArg_ParseTuple(args, "iis#", &sockfd, &type, &str, &size))
		Py_RETURN_NONE;
	MessageQueue::getInstance().MQ2C_Push(sockfd, type, str, size);
	
	Py_RETURN_NONE;
}

static PyObject*
OnTimer(PyObject* self, PyObject* args){
	printf("OnTimer thread_worker %u\n", (unsigned int)pthread_self());
	LogDebug("py->cpp OnTimer");
	int delay;
	int interval;
	if (!PyArg_ParseTuple(args, "ii", &delay, &interval))
		Py_RETURN_NONE;
	LogDebug("py->cpp OnTimer delay=%d,interval=%d",delay,interval);
	unsigned int timerid = Timer::getInstance().timer_add(delay, nullptr, interval);
	LogDebug("py->cpp OnTimer timerid=%d",timerid);
	return Py_BuildValue("i", timerid);
}

static PyMethodDef AlphaMethods[] = {
    {"OnClient", OnClient, METH_VARARGS, "Call client method"},
	{"OnTimer", OnTimer, METH_VARARGS, "Call timer method"},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef alphaModule = {
  PyModuleDef_HEAD_INIT,
  "alphaEngine",           /* name of module */
  "A module that imports an API",  /* Doc string (may be NULL) */
  -1,                 /* Size of per-interpreter state or -1 */
  AlphaMethods       /* Method table */
};

#ifdef __cplusplus
extern "C" {
#endif

PyMODINIT_FUNC
PyInit_alphaEngine(void)
{
	Py_Initialize();
	return PyModule_Create(&alphaModule);
}

#ifdef __cplusplus
}
#endif

WorkerThread::WorkerThread(const char* script_path):pModule_(nullptr),pFunc_(nullptr),pResult_(nullptr){
	
	PyImport_AppendInittab("alphaEngine", PyInit_alphaEngine);
	//call py
	Py_Initialize();

	if (!Py_IsInitialized()){
		LogDebug("py init error\n");
	}

	pModule_ = PyImport_ImportModule("alphaEngine");
	if(pModule_ != nullptr){
		LogDebug("init alpha module success\n");
	}
	else{
		LogDebug("init alpha module error\n");
	}

	char script[128];
	snprintf(script, 128, "../pyscripts/%s/", script_path);
	PyObject *sys_path = PySys_GetObject("path");
	PyList_Append(sys_path, PyUnicode_FromString(script));

	pModule_ = PyImport_ImportModule("pymain");
	if(pModule_ != nullptr){
		LogDebug("init module <%s.pymain>: success\n", script_path);
	}
	else{
		PyErr_Print();
		LogDebug("init module <%s.pymain>: error\n", script_path);
	}

	pResult_ = PyObject_CallMethod(pModule_, "init", "");
	if(pResult_ != nullptr){
		LogDebug("init success\n");
	}
	else{
		LogDebug("init error\n");
	}
}

WorkerThread::~WorkerThread(){
	Py_Finalize();
}

void WorkerThread::OnServer(SP_MessageData q){
	pResult_ = PyObject_CallMethod(pModule_, "OnServer", "iis#", q->Sockfd(), q->Type(), q->Buffer(),q->Size());
	if (pResult_ != nullptr){
		char* ret;
		int result = 0;

		if (PyArg_ParseTuple(pResult_, "i|s",  &result, &ret) == -1)
		{
			LogDebug("error return\n");
		}
		else
		{
			LogDebug("return from py: %d, %s\n", result, ret);
		}
	}
	else{
		LogDebug("pResult_ error\n");
		PyErr_Print();
	}
}
