#include <functional>
#include "thread.h"
#include "thread_timer_test.h"
#include "logger.h"
#include "timer.h"

using namespace alpha;

void timer_func(int timer_id){
	LogDebug("static TimerThread::OnTimer:%d",timer_id);
	//MessageQueue::getInstance().MQ2S_Push(timer_id, FD_TYPE_TIMER, nullptr, 0);
}

ThreadTimerTest::ThreadTimerTest(){

}

ThreadTimerTest::~ThreadTimerTest(){

}

void ThreadTimerTest::Start(){
	void* params = nullptr;
	auto socket_func = std::bind(&ThreadTimerTest::sub_thread, this, std::placeholders::_1);

	std::unique_ptr<Thread> socket_uptr(new Thread(socket_func));
	socket_uptr->start(params);

	auto f_test = std::bind(&ThreadTimerTest::OnTimer, this, std::placeholders::_1);
	Timer::getInstance().set_common_func(std::bind(&ThreadTimerTest::OnTimer, this, std::placeholders::_1));
	//Timer::getInstance().timer_add(1000, nullptr, 4000);
	//timer.timer_add(1000, f_test, 4000);
	Timer::getInstance().timer_add(10000, f_test);

	while(1){
		Timer::getInstance().timer_process();
		usleep(100000);
	}

}

void ThreadTimerTest::sub_thread(void* params){
	usleep(500000);
	Timer::getInstance().timer_add(1000, nullptr, 4000);
}

void ThreadTimerTest::OnTimer(int timer_id){
	LogDebug("TimerThread::OnTimer:%d",timer_id);
}


int main(){

	ThreadTimerTest test;
	test.Start();
	

	return 0;
}