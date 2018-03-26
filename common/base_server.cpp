#include "base_server.h"

namespace alpha{

BaseServer::BaseServer(){

}

BaseServer::~BaseServer(){

}

void BaseServer::LoadConfig(const char* server_name, const char* config_file){
	ConfigReader reader(config_file);
	char* config = reader.GetAllConfig();
	m_json.reset(new JsonHelper(config));
}

void BaseServer::CreateThread(pthread_t* thread, void*(cb)(void*), void* arg){
	if (pthread_create(thread,NULL, cb, arg)) {
		printf("Create thread failed.\n");
		exit(1);
	}
}

struct message_queue* MessageDispatch(){
	return MessageQueue::getInstance().MQ2S_Pop();
}

}