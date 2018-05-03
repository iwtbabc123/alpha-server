/*
*一个MessageData，仅代表一次接收的数据流，不代表一个完整的包，需要手动解包
*/
#ifndef __ALPHA_MESSAGE_DATA_H__
#define __ALPHA_MESSAGE_DATA_H__

#include "util.h"

namespace alpha{

class MessageData{
public:
	MessageData(int sockfd, int type, const char* buffer, int size);

	~MessageData();

	int Sockfd(){return sockfd_;}
	int Type(){return type_;}
	const char* Buffer(){return buffer_;}
	int Size(){return size_;}

private:
	int sockfd_;
	int type_;
	const char* buffer_;
	int size_;

};

}

#endif