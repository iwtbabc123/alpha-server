//#include <Python.h>
#include "gate_server.h"
#include "dispatcher.h"
#include "worker.h"
#include "thread.h"
#include "gate_worker.h"

GateServer::GateServer():worker_uptr_(nullptr){
}

GateServer::~GateServer(){

}

void GateServer::Start(const char* server_name, const char* config_file){
	printf("main thread %u\n", (unsigned int)pthread_self());
	//LoadConfig(server_name, config_file);

	void* params = nullptr;
	auto socket_func = std::bind(&GateServer::thread_socket, this, std::placeholders::_1);

	std::unique_ptr<Thread> socket_uptr(new Thread(socket_func));
	socket_uptr->start(params);

	auto worker_func = std::bind(&GateServer::thread_worker, this, std::placeholders::_1);

	std::unique_ptr<Thread> worker_uptr(new Thread(worker_func));
	worker_uptr->start(params);

	worker_uptr->join();

}

void GateServer::thread_socket(void* params){
	printf("new thread_socket %u\n", (unsigned int)pthread_self());

	Dispatcher::getInstance().StartServer(4002);

}

void GateServer::thread_worker(void* params){
	printf("new thread_worker %u\n", (unsigned int)pthread_self());

	worker_uptr_.reset(new GateWorker());

	auto deal_func = std::bind(&GateWorker::OnServer, worker_uptr_.get(), std::placeholders::_1);
	Worker::getInstance().Start(deal_func);

	printf("new thread_worker end\n");

}