#ifndef __ALPHA_MESSAGE_DATA_H__
#define __ALPHA_MESSAGE_DATA_H__

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