#include <stdio.h>
#include <unistd.h>
#include "timer.h"

using namespace alpha;

void timer_func(void*){
	printf("timer_func\n");
}

int main(){
	Timer timer;
	timer.timer_add(2000, timer_func, nullptr);

	while(1){
		timer.timer_process();
		usleep(100000);
	}
}