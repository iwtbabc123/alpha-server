/*
*逻辑处理
*/
#ifndef __ALPHA_WORKER_H__
#define __ALPHA_WORKER_H__

#include "message_queue.h"

namespace alpha{

class Worker{
public:
	static Worker& getInstance(){
		static Worker instance;
		return instance;
	}

	Worker();
	~Worker();

typedef std::function<void (struct message_queue*)> WorkerFunc;

public:
	void Start(WorkerFunc func);
	struct message_queue* MessageDispatch();
private:


};

}

#endif