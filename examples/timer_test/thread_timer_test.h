#ifndef __THREAD_TIMER_TEST_H__
#define __THREAD_TIMER_TEST_H__

class ThreadTimerTest{

public:
	ThreadTimerTest();
	~ThreadTimerTest();

	void Start();

	void sub_thread(void* params);

	void OnTimer(int timer_id);

};

#endif