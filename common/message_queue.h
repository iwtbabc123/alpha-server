/*
*消息队列
*/
#ifndef __ALPHA_MQ_H__
#define __ALPHA_MQ_H__

#include <pthread.h>
#include <list>
#include "util.h"
#include "message_data.h"

namespace alpha{

typedef std::shared_ptr<MessageData> SP_MessageData;

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

	SP_MessageData MQ2S_Pop();

public:
	void MQ2C_Push(int fd, int type, char* data, int size);
	SP_MessageData MQ2C_Pop();

private:
	bool _Push_With_Notify(SP_MessageData queue);

	void MQ2S_Lock();

	void MQ2S_Unlock();

	void MQ2S_Wait();

	void MQ2S_Signal();

	void MQ2S_Broadcast();  //暂时使用broadcast替换signal

	void MQ2C_Lock();

	void MQ2C_Unlock();


private:
	std::list<SP_MessageData> mq2s_;
	std::list<SP_MessageData> mq2c_;

	pthread_mutex_t mq2s_lock_;
	pthread_cond_t mq2s_cond_;

	pthread_mutex_t mq2c_lock_;

};

}

#endif