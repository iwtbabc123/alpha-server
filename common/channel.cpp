#include "channel.h"
#include "logger.h"

namespace alpha{

Channel::Channel(int fd, int channel_type, struct ev_io* io_watcher)
		:fd_(fd),channel_type_(channel_type),io_watcher_(io_watcher){
	mq_.clear();
}


Channel::~Channel(){
	LogDebug("Channel::~Channel\n");
	close(fd_);

	if (io_watcher_ != nullptr){
		delete io_watcher_;
	}

	for(auto itr = mq_.begin(); itr != mq_.end();){
		mq_.erase(itr++);
	}
}

}