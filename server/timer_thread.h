#ifndef __TIMER_THREAD_H__
#define __TIMER_THREAD_H__

#include "timer.h"
using namespace alpha;

class TimerThread{
public:
	TimerThread();
	~TimerThread();

	void Start();

public:
	void OnTimer(int timer_id);

};

#endif