#include "thread.h"

namespace alpha{

struct Thread_Data{
	typedef Thread::ThreadFunc ThreadFunc;

	ThreadFunc func_;
	void* params_;

	Thread_Data(ThreadFunc func, void* params):func_(std::move(func)),params_(params){
		
	}

};

Thread::Thread(ThreadFunc func):func_(std::move(func)),thread_id_(0){

}

Thread::~Thread(){
	if (started_){
		pthread_detach(thread_id_);
	}
}

void Thread::start(void* params){
	Thread_Data* data = new Thread_Data(func_, params);

	if(pthread_create(&thread_id_, NULL, startThread, data)){
		printf("Create thread failed.\n");
		exit(1);
	}
	printf("thread start thread_id %u\n", (unsigned int)thread_id_);

}

void Thread::join(){
	pthread_join(thread_id_, NULL);
}

void* Thread::startThread(void* params){

	Thread_Data* data = static_cast<Thread_Data*>(params);

	data->func_(data->params_);
}

}