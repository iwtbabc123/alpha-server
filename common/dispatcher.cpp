#include "dispatcher.h"
#include "net_util.h"
#include "logger.h"

namespace alpha{

Dispatcher::Dispatcher():loop_(nullptr),running_(false){

}

Dispatcher::~Dispatcher(){
	if(loop_ != nullptr){
		ev_loop_destroy(loop_);
	}
}

void Dispatcher::StartServer(uint16_t port){
	int fd = netlib_socket();
	if (fd < 0)
	{
		LogError("netlib_socket error:%d",errno);
		exit(EXIT_FAILURE);
	}

	netlib_setnonblocking(fd);

	struct linger linger;
	linger.l_onoff = 1;
	linger.l_linger = 0;
	setsockopt(fd, SOL_SOCKET, SO_LINGER, (const char *) &linger, sizeof(linger));

	if(netlib_bind(fd, port) < 0)
	{
		LogError("netlib_bind error:%d\n",errno);
		exit(EXIT_FAILURE);
	}
	if (netlib_listen(fd,20))
	{
		LogError("netlib_listen error:%d\n",errno);
		exit(EXIT_FAILURE);
	}
	
	loop_ = ev_default_loop(EVBACKEND_EPOLL | EVFLAG_NOENV);

	struct ev_io io_watcher;
	ev_init(&io_watcher, accept_cb);
	AddEvent(&io_watcher, fd, EV_READ);

	//LogInfo("EpollServer::StartServer:listen fd:%d\n",fd);
	
	//InitEventfd();
	//InitTimer();

	ev_run(loop_, 0);
}

int Dispatcher::AddEvent(struct ev_io* ev, int fd, short events){
	ev_io_set(ev, fd, events);
	ev_io_start(loop_, ev);

	return 0;
}
/*
int Dispatcher::UpdateEvent(int fd, short events, Channel* channel)
{	
	//LogDebug("UpdateEvent:%d,%d\n", fd, events);

	struct ev_io* io_watcher = channel->GetIoWatcher();

	if (io_watcher == NULL)
	{
		LogError("UpdateEvent error: io_watcher null\n");
		return -1;
	}
	//TODO, how to update fd event efficiently
	ev_io_stop(loop_, io_watcher);
	ev_io_set(io_watcher, fd, events);
	ev_io_start(loop_, io_watcher);

	return 0;
}

void Dispatcher::RemoveEvent(int fd, Channel* channel)
{
	LogDebug("RemoveEvent: %d\n",fd);
	struct ev_io* io_watcher = channel->GetIoWatcher();
	if (io_watcher == NULL)
	{
		LogError("RemoveEvent error:io_watcher null\n");
		return;
	}
	ev_io_stop(loop_, io_watcher);
}
*/

void Dispatcher::accept_cb(struct ev_loop* loop, struct ev_io* watcher, int revents){
	int fd = watcher->fd;

	if (EV_ERROR & revents)
	{
		//LogDebug("error event in accept\n");
		return;
	}
	printf("accept_cb \n");
	//EpollServer::getSingleton().OnAccept(fd);
}

}
