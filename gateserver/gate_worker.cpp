#include "gate_worker.h"
#include "logger.h"

GateWorker::GateWorker():pModule_(nullptr),pFunc_(nullptr),pResult_(nullptr){
	Py_Initialize();

	if (!Py_IsInitialized())
    {
        LogDebug("py init error\n");
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

	pResult_ = PyObject_CallMethod(pModule_, const_cast<char*>("init"), "");
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



void GateWorker::Start(){
	struct message_queue* q = nullptr;
	while(1){
		LogDebug("GateWorker:Start before\n");
		q = MessageDispatch();
		LogDebug("GateWorker:Start after\n");
		//call python to deal data
		pResult_ = PyObject_CallMethod(pModule_, const_cast<char*>("OnServer"), const_cast<char*>("iis#"), q->sockfd, q->type, q->buffer,q->size);
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

struct message_queue* GateWorker::MessageDispatch(){
	return MessageQueue::getInstance().MQ2S_Pop();
}

