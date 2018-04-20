#ifndef __ALPHA_MQ_H__
#define __ALPHA_MQ_H__

#include <pthread.h>
#include <list>
#include "util.h"

namespace alpha{
//TODO,是否可以工作线程处理socket

struct message_queue{
	int sockfd;
	int type;
	const char* buffer;
	int size;
};


class MessageQueue{

public:
	static MessageQueue& getInstance(){
		static MessageQueue instance;
		return instance;
	}

public:
	MessageQueue();
	~MessageQueue();

	void MQ2S_Push(int fd, int type, const char* buffer, int size);

	struct message_queue* MQ2S_Pop();

private:
	bool _Push_With_Notify(message_queue* queue);

	void MQ2S_Lock();

	void MQ2S_Unlock();

	void MQ2S_Wait();

	void MQ2S_Signal();

	void MQ2S_Broadcast();  //暂时使用broadcast替换signal

	void MQ2C_Lock();

	void MQ2C_Unlock();


private:
	std::list<message_queue*> mq2s_;
	std::list<message_queue*> mq2c_;

	pthread_mutex_t mq2s_lock_;
	pthread_cond_t mq2s_cond_;

	pthread_mutex_t mq2c_lock_;

};

}

#endif