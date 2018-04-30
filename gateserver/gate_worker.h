#ifndef __GATE_WORKER_H__
#define __GATE_WORKER_H__

#include <Python.h>
#include "message_queue.h"

using namespace alpha;

class GateWorker{
public:
	GateWorker();
	~GateWorker();

public:
	void OnServer(struct message_queue* mq);

private:
	PyObject* pModule_;
	PyObject* pFunc_;
	PyObject* pResult_;

};

#endif