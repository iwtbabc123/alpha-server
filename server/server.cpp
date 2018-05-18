#include "server.h"
#include "dispatcher.h"
#include "worker.h"
#include "timer.h"
#include "thread.h"
#include "message_queue.h"
#include "config_reader.h"

Server::Server():worker_uptr_(nullptr),json_uptr_(nullptr){
}

Server::~Server(){

}

void Server::Start(const char* server_name, const char* config_file){
	printf("START SERVER:%s,main thread %u\n", server_name,(unsigned int)pthread_self());
	
	server_name_ = server_name;
	ConfigReader reader(config_file);
	char* config = reader.GetAllConfig();
	json_uptr_.reset(new JsonHelper(config));


	void* params = nullptr;
	auto socket_func = std::bind(&Server::thread_socket, this, std::placeholders::_1);

	std::unique_ptr<Thread> socket_uptr(new Thread(socket_func));
	socket_uptr->start(params);

	auto worker_func = std::bind(&Server::thread_worker, this, std::placeholders::_1);

	std::unique_ptr<Thread> worker_uptr(new Thread(worker_func));
	worker_uptr->start(params);

	worker_uptr->join();

}

void Server::thread_socket(void* params){
	printf("new thread_socket %u\n", (unsigned int)pthread_self());

	int port;
	json_uptr_->GetJsonItem2(server_name_.c_str(), "port", port);
	Dispatcher::getInstance().StartServer(port);

}

void Server::thread_worker(void* params){
	printf("new thread_worker %u\n", (unsigned int)pthread_self());

	string script_path;
	json_uptr_->GetJsonItem2(server_name_.c_str(), "script_path", script_path);

	worker_uptr_.reset(new WorkerThread(script_path.c_str()));

	auto deal_func = std::bind(&WorkerThread::OnServer, worker_uptr_.get(), std::placeholders::_1);
	Worker::getInstance().Start(deal_func);

	printf("new thread_worker end\n");

}

void Server::thread_timer(void* params){
	printf("new thread_timer %u\n", (unsigned int)pthread_self());

	Timer timer;
	timer.timer_add(1000, timer_func, nullptr);

	timer.timer_add(1500, timer_func2, nullptr, false, 2);

	while(1){
		timer.timer_process();
		usleep(100000);
	}
}