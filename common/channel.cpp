#include "channel.h"
#include "logger.h"

namespace alpha{

Channel::Channel(int fd, int fd_type, struct ev_io* io_watcher):fd_(fd),fd_type_(fd_type),io_watcher_(io_watcher){
	mq_.clear();
	if (fd_type == FD_TYPE_CLIENT){
		success_ = true;
	}
	else if(fd_type == FD_TYPE_SERVER){
		success_ = false;
	}
	else{
		success_ = false;
	}
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