#ifndef __ALPHA_CHANNEL_H__
#define __ALPHA_CHANNEL_H__

#include <ev.h>
#include "util.h"
#include "message_queue.h"  //TODO,把struct抽出来

namespace alpha{

class Channel{
	public:
		Channel(int fd, struct ev_io* io_watcher);
		virtual ~Channel();

		int Fd(){return fd_;}

		struct ev_io* GetIoWatcher(){return io_watcher_;}
		void SetIoWatcher(struct ev_io* io_watcher){io_watcher_ = io_watcher;}

		bool empty(){return mq_.empty();}
		bool push_back(message_queue* mq){mq_.push_back(mq);}
		struct message_queue* pop_front(){
			if (mq_.empty()){
				return nullptr;
			}
			struct message_queue* queue = mq_.front();
			mq_.pop_front();
			return queue;
		}

	protected:
		int fd_;
		//int fd_type_;
	private:
		struct ev_io* io_watcher_;

		std::list<message_queue*> mq_;
};

}

#endif

