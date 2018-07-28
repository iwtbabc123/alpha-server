#include <stdio.h>
#include <unistd.h>
#include "timer.h"

using namespace alpha;

void timer_func(int timer_id){
	printf("timer_func:%d\n",timer_id);
}

void timer_func2(int timer_id){
	printf("timer_func2\n");
}



int main(){
	auto f_test = std::bind(timer_func, std::placeholders::_1);
	Timer::getInstance().set_common_func(f_test);
	Timer::getInstance().timer_add(1000, nullptr, 4000);
	//timer.timer_add(1000, f_test, 4000);
	Timer::getInstance().timer_add(10000, f_test);

	while(1){
		Timer::getInstance().timer_process();
		usleep(100000);
	}
}