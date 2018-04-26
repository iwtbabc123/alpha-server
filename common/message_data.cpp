#include "message_data.h"
#include "util.h"

namespace alpha{

MessageData::MessageData(int sockfd, int type, const char* buffer, int size)
	:sockfd_(sockfd),type_(type),buffer_(buffer),size_(size){
}

MessageData::~MessageData(){
	if (buffer_ != nullptr){
		free((char*)buffer_);
		buffer_ = nullptr;
	}
}

}