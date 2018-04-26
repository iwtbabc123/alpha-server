#include "base_server.h"

namespace alpha{

BaseServer::BaseServer(){

}

BaseServer::~BaseServer(){

}

void BaseServer::LoadConfig(const char* server_name, const char* config_file){
	ConfigReader reader(config_file);
	char* config = reader.GetAllConfig();
	json_helper_.reset(new JsonHelper(config));
}

MessageData* MessageDispatch(){
	return MessageQueue::getInstance().MQ2S_Pop();
}

}