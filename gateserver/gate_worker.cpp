#include "gate_worker.h"
#include "logger.h"

static PyObject*
OnClient(PyObject* self, PyObject* args)
{
	LogDebug("py->cpp call_client\n");

	int sockfd;
	int type;
	char* str;
	int size;
	if (!PyArg_ParseTuple(args, "iis#", &sockfd, &type, &str, &size))
		Py_RETURN_NONE;
	MessageQueue::getInstance().MQ2C_Push(sockfd, type, str, size);
	
	Py_RETURN_NONE;
}

static PyMethodDef AlphaMethods[] = {
    {"OnClient", OnClient, METH_VARARGS, "Call client method"},
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

GateWorker::GateWorker():pModule_(nullptr),pFunc_(nullptr),pResult_(nullptr){
	
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

	PyRun_SimpleString("import sys");
	PyRun_SimpleString("sys.path.insert(0, '../pyscripts/gate/')"); 

	pModule_ = PyImport_ImportModule("pymain");
	if(pModule_ != nullptr){
		LogDebug("init module success\n");
	}
	else{
		LogDebug("init module error\n");
	}

	pResult_ = PyObject_CallMethod(pModule_, "init", "");
	if(pResult_ != nullptr){
		LogDebug("init success\n");
	}
	else{
		LogDebug("init error\n");
	}

}

GateWorker::~GateWorker(){
	Py_Finalize();
}

void GateWorker::OnServer(struct message_queue* q){
	pResult_ = PyObject_CallMethod(pModule_, "OnServer", "iis#", q->sockfd, q->type, q->buffer,q->size);
	if (pResult_ != NULL){
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
	}
}
/*
void GateWorker::Start(){
	struct message_queue* q = nullptr;
	while(1){
		LogDebug("GateWorker:Start before\n");
		q = MessageDispatch();
		LogDebug("GateWorker:Start after\n");
		//call python to deal data
		pResult_ = PyObject_CallMethod(pModule_, "OnServer", "iis#", q->sockfd, q->type, q->buffer,q->size);
		if (pResult_ != NULL){
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
		}
		//free(q->buffer);
	}
}
*/
/*
struct message_queue* GateWorker::MessageDispatch(){
	return MessageQueue::getInstance().MQ2S_Pop();
}
*/

