#ifndef __ALPHA_CHANNEL_H__
#define __ALPHA_CHANNEL_H__

#include <ev.h>
#include "util.h"

namespace alpha{

class Channel{
	public:
		Channel(int fd, struct ev_io* io_watcher);  //TODO, add fd_type
		virtual ~Channel();

		int Fd(){return fd_;}

		struct ev_io* GetIoWatcher(){return io_watcher_;}
		void SetIoWatcher(struct ev_io* io_watcher){io_watcher_ = io_watcher;}

	protected:
		int fd_;
	private:
		struct ev_io* io_watcher_;
};

}

#endif

