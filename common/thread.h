#ifndef __ALPHA_THREAD_H__
#define __ALPHA_THREAD_H__

#include <functional>
#include <pthread.h>

namespace alpha{

class Thread{

public:
	typedef std::function<void (void* params)> ThreadFunc;

	Thread(ThreadFunc func);

	~Thread();

	void start(void* params);

	void join();

	static void* startThread(void* params);

private:
	ThreadFunc func_;

	pthread_t thread_id_;

	bool started_;
	bool joined_;

};

}

#endif