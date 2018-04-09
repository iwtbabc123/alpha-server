#include "channel.h"

namespace alpha{

Channel::Channel(int fd, struct ev_io* io_watcher):fd_(fd),io_watcher_(io_watcher){

}


Channel::~Channel()
{
	//LogDebug("Channel::~Channel\n");
	close(fd_);

	if (io_watcher_ != nullptr)
	{
		delete io_watcher_;
	}
}

}