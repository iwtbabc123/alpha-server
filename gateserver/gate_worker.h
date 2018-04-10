#ifndef __GATE_WORKER_H__
#define __GATE_WORKER_H__

#include <Python.h>
#include "message_queue.h"

using namespace alpha;

class GateWorker{
public:
	static GateWorker& getInstance(){
		static GateWorker instance;
		return instance;
	}

	GateWorker();
	~GateWorker();

public:
	void Start();

private:
	struct message_queue* MessageDispatch();

private:
	PyObject* pModule_;
	PyObject* pFunc_;
	PyObject* pResult_;

};

#endif