#ifndef __ALPHA_THREAD_H__
#define __ALPHA_THREAD_H__

#include <functional>
#include <pthread.h>

namespace alpha{

typedef std::function<void (void* params)> ThreadFunc;

struct Thread_Data{
	ThreadFunc func_;

	Thread_Data(ThreadFunc func):func_(std::move(func)){
		
	}

};

class Thread{

public:
	Thread();

	~Thread();

	void start(void* params);

	void join();

	static void* startThread(void* params);

private:
	pthread_t thread_id_;

	bool started_;
	bool joined_;

};

}

#endif