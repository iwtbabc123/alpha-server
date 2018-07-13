#include "worker_thread.h"
#include "timer.h"
#include "logger.h"

static PyObject*
OnSocket(PyObject* self, PyObject* args){
	int sockfd;
	int type;
	char* str;
	int size;
	if (!PyArg_ParseTuple(args, "iis#", &sockfd, &type, &str, &size)){
		PyErr_Print();
		Py_RETURN_NONE;
	}
	LogDebug("py->cpp OnSocket");
	MessageQueue::getInstance().MQ2C_Push(sockfd, type, str, size);
	
	Py_RETURN_NONE;
}

static PyObject*
OnTimer(PyObject* self, PyObject* args){
	printf("OnTimer thread_worker %u\n", (unsigned int)pthread_self());
	LogDebug("py->cpp OnTimer");
	int delay;
	int interval;
	if (!PyArg_ParseTuple(args, "ii", &delay, &interval)){
		PyErr_Print();
		Py_RETURN_NONE;
	}
	LogDebug("py->cpp OnTimer delay=%d,interval=%d",delay,interval);
	unsigned int timerid = Timer::getInstance().timer_add(delay, nullptr, interval);
	LogDebug("py->cpp OnTimer timerid=%d",timerid);
	return Py_BuildValue("i", timerid);
}

static PyObject*
OnConnectServer(PyObject* self, PyObject* args){
	char* ip;
	int size;
	int port;
	if (!PyArg_ParseTuple(args, "is#", &port, &ip, &size)){
		PyErr_Print();
		Py_RETURN_NONE;
	}
	LogDebug("py->cpp OnConnectServer ip=%s,size=%d,port=%d",ip,size,port);
	MessageQueue::getInstance().MQ2C_Push(port, FD_TYPE_CONNECT, ip, size);
	Py_RETURN_NONE;
}

static PyMethodDef AlphaMethods[] = {
	{"OnSocket", OnSocket, METH_VARARGS, "Call socket method"},
	{"OnTimer", OnTimer, METH_VARARGS, "Call timer method"},
	{"OnConnectServer", OnConnectServer, METH_VARARGS, "Call connect server method"},
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

WorkerThread::WorkerThread(const char* server_name, const char* script_path):pModule_(nullptr),pFunc_(nullptr),pResult_(nullptr){
	
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

	pResult_ = PyObject_CallMethod(pModule_, "init", "s#", server_name, strlen(server_name));
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

void WorkerThread::OnWorkerLogic(SP_MessageData q){
	int fd_type = q->Type();
	const char* func_name = nullptr;

	switch (fd_type){
		case FD_TYPE_ACCEPT:
		case FD_TYPE_CLIENT:
		case FD_TYPE_CLOSE:{
			func_name = "OnClientProxy";
			break;
		}
		case FD_TYPE_CONNECT:
		case FD_TYPE_SERVER:{
			func_name = "OnServerProxy";
			break;
		}
		default:
			break;
	}

	if (func_name == nullptr){
		LogError("OnWorkerLogic error:fd_type=%d\n", fd_type);
		return;
	}

	pResult_ = PyObject_CallMethod(pModule_, func_name, "iis#", q->Sockfd(), q->Type(), q->Buffer(),q->Size());
	if (pResult_ != nullptr){
		char* ret;
		int result = 0;

		if (PyArg_ParseTuple(pResult_, "i|s",  &result, &ret) == -1){
			LogDebug("error return\n");
		}
		else{
			LogDebug("return from py: %d, %s\n", result, ret);
		}
	}
	else{
		LogDebug("pResult_ error\n");
		PyErr_Print();
	}
}
