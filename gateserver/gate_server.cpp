//#include <Python.h>
#include "gate_server.h"
#include "dispatcher.h"
#include "worker.h"
#include "thread.h"
#include "gate_worker.h"

GateServer::GateServer(){
}

GateServer::~GateServer(){

}

void GateServer::Start(const char* server_name, const char* config_file){
	printf("main thread %u\n", (unsigned int)pthread_self());
	//LoadConfig(server_name, config_file);

	void* params = nullptr;
	auto func_socket = std::bind(&GateServer::thread_socket, this, std::placeholders::_1);

	std::unique_ptr<Thread> uni_ptr1(new Thread(func_socket));
	uni_ptr1->start(params);

	auto func_worker = std::bind(&GateServer::thread_worker, this, std::placeholders::_1);

	std::unique_ptr<Thread> uni_ptr2(new Thread(func_worker));
	uni_ptr2->start(params);

	uni_ptr2->join();

}

void GateServer::thread_socket(void* params){
	printf("new thread_socket %u\n", (unsigned int)pthread_self());

	Dispatcher::getInstance().StartServer(4002);

}

void GateServer::thread_worker(void* params){
	printf("new thread_worker %u\n", (unsigned int)pthread_self());

	//GateWorker::getInstance().Start();
	auto deal_mq_func = std::bind(&GateWorker::OnServer, &GateWorker::getInstance(), std::placeholders::_1);
	Worker::getInstance().Start(deal_mq_func);

}