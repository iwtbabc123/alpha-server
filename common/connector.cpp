#include "connector.h"

namespace alpha{

Connector::Connector(int fd, const char* server_ip, uint16_t port):Channel(fd, nullptr),
		server_ip_(server_ip),port_(port),success_(false){

}

Connector::~Connector(){

}

}