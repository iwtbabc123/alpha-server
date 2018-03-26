#include<stdio.h>
#include <unistd.h>
#include<memory>
#include "thread_test.h"

Thread_test::Thread_test():int_val_(1){

}

void Thread_test::start(){
	printf("start thread test %d, %u\n",int_val_, (unsigned int)pthread_self());

	void* ttt = nullptr;
	auto f_test = std::bind(&Thread_test::new_thread_test,this, std::placeholders::_1);

	std::unique_ptr<Thread> test_thread (new Thread(f_test));
	int_val_ = 2;
	test_thread->start(ttt);

	test_thread->join();
}

void Thread_test::new_thread_test(void* params){
	printf("new thread test %d, %u\n", int_val_, (unsigned int)pthread_self());

	sleep(100);
}


int main(){

	Thread_test test;
	test.start();

}