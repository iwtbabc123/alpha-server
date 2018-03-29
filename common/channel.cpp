#include "channel.h"

namespace alpha
{

Channel::Channel(int fd, struct ev_io* io_watcher, EFDTYPE fdtype):fd_(fd),io_watcher_(io_watcher),fdtype_(fdtype)
{

}


Channel::~Channel()
{
	//LogDebug("Channel::~Channel\n");
	close(fd_);

	if (io_watcher_ != NULL)
	{
		delete io_watcher_;
	}
}

}