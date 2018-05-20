#include <unistd.h>
#include "timer_thread.h"
#include "message_queue.h"
#include "logger.h"

void timer_test(int timer_id){
	LogDebug("static TimerThread::OnTimer:%d",timer_id);
	MessageQueue::getInstance().MQ2S_Push(timer_id, FD_TYPE_TIMER, nullptr, 0);
}

TimerThread::TimerThread(){

}

TimerThread::~TimerThread(){

}

void TimerThread::Start(){
	LogDebug("TimerThread::Start");
	//这里用auto会报错
	//TimerFunc on_timer_func = std::bind(&TimerThread::OnTimer, this, std::placeholders::_1);
	Timer::getInstance().set_common_func(std::bind(&TimerThread::OnTimer, this, std::placeholders::_1));
	Timer::getInstance().timer_add(3000, nullptr, 3000);
	while(1){
		Timer::getInstance().timer_process();
		usleep(100000);  //100ms
	}
}

void TimerThread::OnTimer(int timer_id){
	LogDebug("TimerThread::OnTimer:%d",timer_id);
	MessageQueue::getInstance().MQ2S_Push(timer_id, FD_TYPE_TIMER, nullptr, 0);
}