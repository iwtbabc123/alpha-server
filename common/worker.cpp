#include "worker.h"
#include "logger.h"

namespace alpha{

Worker::Worker(){

}

Worker::~Worker(){

}

void Worker::Start(WorkerFunc func){
	MessageData* q = nullptr;
	while(1){
		LogDebug("Worker:Start start=================>\n");
		q = MessageDispatch();
		func(q);
		LogDebug("Worker:Start end===================<\n");
		delete q;
		q = nullptr;

	}
}

	MessageData* Worker::MessageDispatch(){
	return MessageQueue::getInstance().MQ2S_Pop();
}

}
