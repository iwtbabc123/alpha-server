#include "gate_worker.h"
#include "logger.h"

GateWorker::GateWorker():pModule_(NULL),pFunc_(NULL),pResult_(NULL){
	Py_Initialize();

	PyRun_SimpleString("import sys");
	PyRun_SimpleString("sys.path.append('../pyscripts/')"); 

	pModule_ = PyImport_ImportModule("pymain");

	pResult_ = PyObject_CallMethod(pModule_, const_cast<char*>("init"), "");

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
		pResult_ = PyObject_CallMethod(pModule_, const_cast<char*>("OnServer"), const_cast<char*>("iis"), q->sockfd, q->type, q->buffer);
		if (pResult_ != NULL){
			char* ret;
			int result = 0;

			if (PyArg_ParseTuple(pResult_, "i|s",  &result, &ret) == -1)
			{
				LogDebug("error return\n");
			}
			else
			{
				//LogDebug("return from py: %d, %s\n", result, ret);
			}
		}
	}
}

struct message_queue* GateWorker::MessageDispatch(){
	return MessageQueue::getInstance().MQ2S_Pop();
}

