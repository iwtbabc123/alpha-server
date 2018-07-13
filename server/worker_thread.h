#ifndef __WORKER_THREAD_H__
#define __WORKER_THREAD_H__

#include <Python.h>
#include "message_queue.h"

using namespace alpha;

class WorkerThread{
public:
	WorkerThread(const char* server_name, const char* script_path);
	~WorkerThread();

public:
	void OnWorkerLogic(SP_MessageData mq);

private:
	PyObject* pModule_;
	PyObject* pFunc_;
	PyObject* pResult_;

};

#endif