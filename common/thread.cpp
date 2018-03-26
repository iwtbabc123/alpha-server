#include "thread.h"

namespace alpha{

Thread::Thread():thread_id_(0){

}

Thread::~Thread(){
	if (started_){
		pthread_detach(thread_id_);
	}
}

void Thread::start(void* params){
	pthread_create(&thread_id_, NULL, startThread, params);
}

void Thread::join(){
	pthread_join(thread_id_, NULL);
}

void* Thread::startThread(void* params){

	Thread_Data* data = static_cast<Thread_Data*>(params);

	data->func_(params);
}

}