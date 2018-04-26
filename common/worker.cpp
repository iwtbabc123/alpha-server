#include "worker.h"
#include "logger.h"

namespace alpha{

Worker::Worker(){

}

Worker::~Worker(){

}

void Worker::Start(WorkerFunc func){
	while(1){
		LogDebug("Worker:Start start=================>\n");
		SP_MessageData q = MessageDispatch();
		func(q);
		LogDebug("Worker:Start end===================<\n");
	}
}

SP_MessageData Worker::MessageDispatch(){
	return MessageQueue::getInstance().MQ2S_Pop();
}

}
