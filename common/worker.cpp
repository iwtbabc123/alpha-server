#include "worker.h"
#include "logger.h"

namespace alpha{

Worker::Worker(){

}

Worker::~Worker(){

}

void Worker::Start(WorkerFunc func){
	struct message_queue* q = nullptr;
	while(1){
		LogDebug("GateWorker:Start before\n");
		q = MessageDispatch();
		func(q);
		delete q;
		q = nullptr;

	}
}

struct message_queue* Worker::MessageDispatch(){
	return MessageQueue::getInstance().MQ2S_Pop();
}

}
