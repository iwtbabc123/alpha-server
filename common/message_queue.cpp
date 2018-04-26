#include "message_queue.h"
#include "logger.h"
#include "net_util.h"
#include "dispatcher.h"

namespace alpha{

MessageQueue::MessageQueue(){
	
	pthread_mutex_init(&mq2s_lock_, NULL);
	pthread_cond_init(&mq2s_cond_, NULL);

	pthread_mutex_init(&mq2c_lock_, NULL);

}

MessageQueue::~MessageQueue(){

	pthread_cond_destroy(&mq2s_cond_);

	if (!mq2s_.empty()){
		for(auto itr = mq2s_.begin(); itr != mq2s_.end();){
			mq2s_.erase(itr++);
		}
	}

	if (!mq2c_.empty())
	{
		for(auto itr2 = mq2c_.begin(); itr2 != mq2c_.end();){
			mq2c_.erase(itr2++);
		}
	}
}

void MessageQueue::MQ2S_Push(int fd, int type, const char* buffer, int size){
	MQ2S_Lock();

	SP_MessageData queue(new MessageData(fd,type, buffer, size));
	mq2s_.push_back(queue);

	MQ2S_Signal();
	
	MQ2S_Unlock();
}

	SP_MessageData MessageQueue::MQ2S_Pop(){

	MQ2S_Lock();
	LogDebug("mq2s_pop before");
	while(mq2s_.empty()){
		MQ2S_Wait();
	}
	LogDebug("mq2s_pop enter");

	SP_MessageData queue = mq2s_.front();
	mq2s_.pop_front();

	MQ2S_Unlock();

	return queue;
}

void MessageQueue::MQ2C_Push(int fd, int type, char* data, int size){

	LogDebug("MessageQueue::mq2c_Push:%d,%d,%s,%d\n",fd, type ,data, size);
	MQ2C_Lock();
	
	char* buffer = (char*)malloc(sizeof(char) * size);
	memcpy(buffer, data, size);

	SP_MessageData queue(new MessageData(fd, type, buffer, size));
	mq2c_.push_back(queue);

	int ret = netlib_eventfd_write(Dispatcher::getInstance().Eventfd());
	if (ret != 0)
	{
		LogError("EpollServer::eventfd write error\n");
	}

	MQ2C_Unlock();
}

	SP_MessageData MessageQueue::MQ2C_Pop(){
	LogDebug("MessageQueue::mq2c_Pop\n");
	MQ2C_Lock();

	if (mq2c_.empty())
	{
		MQ2C_Unlock();  //forgot it
		return nullptr;
	}
	SP_MessageData queue = mq2c_.front();
	mq2c_.pop_front();

	MQ2C_Unlock();
	return queue;
}

bool MessageQueue::_Push_With_Notify(SP_MessageData queue)
{
	bool notify = false;
	if (mq2s_.empty())
	{
		notify = true;
	}

	mq2s_.push_back(queue);
	return notify;

}

void MessageQueue::MQ2S_Lock()
{
	pthread_mutex_lock(&mq2s_lock_);
}

void MessageQueue::MQ2S_Unlock()
{
	pthread_mutex_unlock(&mq2s_lock_);
}

void MessageQueue::MQ2S_Wait()
{
	pthread_cond_wait(&mq2s_cond_, &mq2s_lock_);
}

void MessageQueue::MQ2S_Signal()
{
	pthread_cond_signal(&mq2s_cond_);
}

void MessageQueue::MQ2S_Broadcast()
{
	pthread_cond_broadcast(&mq2s_cond_);
}

void MessageQueue::MQ2C_Lock()
{
	pthread_mutex_lock(&mq2c_lock_);
}

void MessageQueue::MQ2C_Unlock()
{
	pthread_mutex_unlock(&mq2c_lock_);
}

}