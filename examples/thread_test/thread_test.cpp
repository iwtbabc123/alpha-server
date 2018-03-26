#include<stdio.h>
#include<memory>
#include "thread_test.h"

Thread_test::Thread_test():int_val_(1){

}

void Thread_test::start(){
	printf("start thread test %d\n",int_val_);

	void* ttt = nullptr;
	std::function<void(void*)> f_test = std::bind(&Thread_test::new_thread_test,this, ttt);

	std::unique_ptr<Thread> test_thread (new Thread());

	Thread_Data *data = new Thread_Data(f_test);
	int_val_ = 2;
	test_thread->start(data);

	test_thread->join();

	delete data;
}

void Thread_test::new_thread_test(void* params){
	printf("new thread test %d\n", int_val_);
}


int main(){

	Thread_test test;
	test.start();

}