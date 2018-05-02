#include <stdio.h>
#include <unistd.h>
#include "timer.h"

using namespace alpha;

void timer_func(void*){
	printf("timer_func\n");
}

void timer_func2(void*){
	printf("timer_func2\n");
}

int main(){
	Timer timer;
	timer.timer_add(1000, timer_func, nullptr);

	timer.timer_add(1500, timer_func2, nullptr, false, 2);

	while(1){
		timer.timer_process();
		usleep(100000);
	}
}