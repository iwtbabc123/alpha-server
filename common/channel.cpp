#include "channel.h"
#include "logger.h"

namespace alpha{

Channel::Channel(int fd, struct ev_io* io_watcher):fd_(fd),io_watcher_(io_watcher){
	mq_.clear();
}


Channel::~Channel(){
	LogDebug("Channel::~Channel\n");
	close(fd_);

	if (io_watcher_ != nullptr)
	{
		delete io_watcher_;
	}

	for(auto itr = mq_.begin(); itr != mq_.end(); itr++){
		MessageData* mq = * itr;
		delete mq;
	}
}

}