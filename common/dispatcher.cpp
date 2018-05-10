#include "dispatcher.h"
#include "message_queue.h"
#include "net_util.h"
#include "logger.h"

namespace alpha{

Dispatcher::Dispatcher():loop_(nullptr),running_(false),eventfd_(0){

}

Dispatcher::~Dispatcher(){
	if(loop_ != nullptr){
		ev_loop_destroy(loop_);
	}

	close(eventfd_);
}

void Dispatcher::StartServer(uint16_t port){
	int fd = netlib_socket();
	if (fd < 0){
		LogError("netlib_socket error:%d",errno);
		exit(EXIT_FAILURE);
	}

	netlib_setnonblocking(fd);

	struct linger linger;
	linger.l_onoff = 1;
	linger.l_linger = 0;
	setsockopt(fd, SOL_SOCKET, SO_LINGER, (const char *) &linger, sizeof(linger));

	netlib_reuse_port(fd, true);

	if(netlib_bind(fd, port) < 0){
		LogError("netlib_bind error:%d\n",errno);
		exit(EXIT_FAILURE);
	}
	if (netlib_listen(fd,20)){
		LogError("netlib_listen error:%d\n",errno);
		exit(EXIT_FAILURE);
	}
	
	loop_ = ev_default_loop(EVBACKEND_EPOLL | EVFLAG_NOENV);

	struct ev_io io_watcher;
	ev_init(&io_watcher, accept_cb);
	AddEvent(&io_watcher, fd, EV_READ);

	LogInfo("Dispatcher::StartServer:listen fd:%d\n",fd);
	
	InitEventFd();
	InitTimer();

	ev_run(loop_, 0);
}

/*
*此进程作为client连接某个server,
*eg: gate->game,game->db.
*/
void Dispatcher::ConnectIpPort(const char* ip, uint16_t port){
	LogDebug("Dispatcher::ConnectIpPort ip=%s,port=%d\n", ip, port);

	bool flag = true;

	do{
		int conn_fd = netlib_socket();
		if (conn_fd < 0){
			LogError("Dispatcher::ConnectIpPort socket error");
			continue;
		}
		flag = false;
		SP_Connector connector(new Connector(conn_fd, ip, port));
		connector_map_[conn_fd] = connector;
	}while(flag);
}

void Dispatcher::OnAccept(int fd){
	LogDebug("EpollServer::OnAccept %d\n", fd);

	int conn_fd = netlib_accept(fd);
	if (conn_fd < 0){
		LogError("accept error\n");
	}

	netlib_setnonblocking(conn_fd);

	struct ev_io* conn_ev = (struct ev_io*) malloc(sizeof(struct ev_io));
	if (conn_ev == nullptr){
		LogError("malloc error in accept_cb\n");
		return;
	}

	ev_init(conn_ev, r_w_cb);
	AddEvent(conn_ev, conn_fd, EV_READ);
	AddChannel(conn_ev, conn_fd);

	MessageQueue::getInstance().MQ2S_Push(conn_fd, FD_TYPE_ACCEPT, nullptr, 0);

	//free(conn_ev);

}

void Dispatcher::OnRead(int fd, int fd_type){
	LogDebug("Dispatcher::OnRead:%d\n", fd);

	if (fd_type == FD_TYPE_ACCEPT){
		char buffer[READ_BUF_SIZE] = {0};

		int bytes = netlib_recv(fd, buffer, READ_BUF_SIZE);
		if (bytes == 0){  //close
			//remote close fd actively
			RemoveEvent(fd);
			OnFdClosed(fd);
			LogInfo("Dispatcher::OnRead remote close fd: %d\n", fd);
			MessageQueue::getInstance().MQ2S_Push(fd, FD_TYPE_CLOSE, NULL, bytes);
		}
		else if(bytes < 0){  //error
			RemoveEvent(fd);
			OnFdClosed(fd);
			LogInfo("Dispatcher::OnRead fd error\n");
		}
		else{
			char* socket_data = (char*)malloc(sizeof(char) * bytes);
			memcpy(socket_data, buffer, bytes);
			//std::string str_buf(buffer);
			LogInfo("Dispatcher::OnRead %d bytes\n", bytes);
			MessageQueue::getInstance().MQ2S_Push(fd, FD_TYPE_READ, socket_data, bytes);
		}
	}
}

void Dispatcher::OnWrite(int fd, int fd_type){
	LogDebug("EpollServer::OnWrite:%d\n",fd);
	
	if (fd_type == FD_TYPE_ACCEPT){
		auto channel = this->GetChannel(fd);
		if (channel == nullptr)
		{
			LogError("EpollServer::OnWrite channel null\n");
			return;
		}

		int events = EV_READ;

		while(!channel->empty())
		{
			auto mq = channel->pop_front();

			LogDebug("EpollServer::OnWrite send_len %d\n", mq->Size());

			char* tmp = (char*)malloc(sizeof(char) * mq->Size());
			memcpy(tmp, mq->Buffer(), mq->Size());
			//TODO,只发送一部分mq，剩余的尚未处理
			int ret = netlib_send(fd, tmp, mq->Size());
			if (ret == -1)  //TODO,发送不成功要重新发送
			{
				LogWarning("netlib_send -1\n");
				//
				//UpdateEvent(fd, EPOLLIN | EPOLLOUT);
				events |= EV_WRITE;
				break;
			}
			else if (ret == 0)
			{	
				LogDebug("netlib_send 0\n");
				break;
			}
			else if (ret > 0)
			{
				LogDebug("netlib_send %d\n", ret);
			}
		}

		UpdateEvent(fd, events, channel);
	}
}

void Dispatcher::OnEventfd(int efd)
{
	LogDebug("EpollServer::OnEventfd %d\n",efd);
	if (efd != eventfd_)
	{
		LogError("EpollServer::OnEventfd error %d != %d\n",efd, eventfd_);
	}

	int ret = netlib_eventfd_read(eventfd_);
	if (ret != 0)
	{
		LogError("EpollServer::eventfd read error\n");
		return;
	}

	while(true){
		auto mq = MessageQueue::getInstance().MQ2C_Pop();
		if (mq == nullptr)
			break;
		if (mq->Type() == FD_TYPE_CLIENT){
			auto channel = GetChannel(mq->Sockfd());

			if (channel == nullptr)
			{
				LogWarning("EpollServer::OnEventfd channel null\n");
				continue;
			}

			channel->push_back(mq);

			//update channel
			int events = EV_READ;
			if (!channel->empty())
			{
				events |= EV_WRITE;
			}
			UpdateEvent(mq->Sockfd(), events, channel);
		}
		else if(mq->Type() == FD_TYPE_SERVER){

		}
		/*
		else if (mq->type == MQ_TYPE_BROADCAST)
		{
			Broadcast* broadcast = mq->broad;
			list<uint32_t>& uniqids = broadcast->uniqids;
			while(!uniqids.empty())
			{
				uint32_t uniqid = uniqids.front();
				uniqids.pop_front();
				//same with MQ_TYPE_PACK
				int fd = GetFdFromUniqid(uniqid);
				Channel* channel = GetChannel(fd);

				if (channel == NULL)
				{
					LogWarning("EpollServer::OnEventfd channel null\n");
					continue;
				}

				channel->OutBuffer().Write(broadcast->pack->GetBuffer(), broadcast->pack->GetTotalLength());

				//update channel
				int events = EV_READ;
				if (channel->OutBuffer().GetWriteOffset() > 0)
				{
					events |= EV_WRITE;
				}
				UpdateEvent(fd, events, channel);
			}

			delete broadcast->pack;
			broadcast->pack = NULL;
			delete broadcast;
			broadcast = NULL;
			delete mq;
			mq = NULL;

		}
		else if (mq->type == MQ_TYPE_TIMER)
		{
			struct ev_timer* timeout_watcher = (struct ev_timer*) malloc(sizeof(struct ev_timer));
			
			TimerStruct* timer_struct = mq->timer;

			Timer* timer = new Timer(timer_struct->timerid, timer_struct->repeat_sec, timeout_watcher);
			timer_map_.insert(pair<uint32_t, Timer*>(1, timer));

			ev_timer_init(timeout_watcher, timeout_cb, timer_struct->delay, timer_struct->repeat_sec);
			ev_timer_start(loop_, timeout_watcher);
			//LogWarning("EpollServer::OnEventfd timer: %d,%d,%d\n", timer_struct->timerid, timer_struct->delay, timer_struct->repeat_sec);
		}
		else if (mq->type == MQ_TYPE_CONNECT)
		{
			Connector* connector = GetUserfulConnector();
			if (connector == NULL)
			{
				//LOG_ERROR("EpollServer::OnEventfd connector null");
				delete mq->pack;
				delete mq;
				continue;
			}

			int fd = connector->Fd();

			connector->OutBuffer().Write(mq->pack->GetBuffer(), mq->pack->GetTotalLength());

			delete mq->pack;
			mq->pack = NULL;
			delete mq;
			mq = NULL;

			//update channel
			int events = EV_READ;
			if (connector->OutBuffer().GetWriteOffset() > 0)
			{
				events |= EV_WRITE;  //then, 
			}
			
			UpdateEvent(fd, events, connector);
		}
		*/
		else
		{
			LogError("EpollServer::OnEventfd type error:%d\n",mq->Type());
			continue;
		}
	}
}

void Dispatcher::OnTimer(){
	ConnectOtherServer();
}

int Dispatcher::AddEvent(struct ev_io* ev, int fd, short events){
	ev_io_set(ev, fd, events);
	ev_io_start(loop_, ev);

	return 0;
}

int Dispatcher::UpdateEvent(int fd, short events, SP_Channel channel)
{	
	//LogDebug("UpdateEvent:%d,%d\n", fd, events);

	struct ev_io* io_watcher = channel->GetIoWatcher();

	if (io_watcher == nullptr)
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

void Dispatcher::RemoveEvent(int fd){
	LogDebug("RemoveEvent: %d\n",fd);

	auto channel = this->GetChannel(fd);
	if(channel == nullptr){
		return;
	}

	struct ev_io* io_watcher = channel->GetIoWatcher();
	if (io_watcher == nullptr){
		LogError("RemoveEvent error:io_watcher null\n");
		return;
	}
	ev_io_stop(loop_, io_watcher);
}


SP_Channel Dispatcher::GetChannel(int fd)
{
	auto iter = channel_map_.find(fd);
	if (iter == channel_map_.end()){
		return nullptr;
	}
	else{
		return iter->second;
	}
}

void Dispatcher::AddChannel(struct ev_io* io_watcher, int fd)
{
	auto iter = channel_map_.lower_bound(fd);
	if (iter != channel_map_.end() && iter->first == fd){
		LogWarning("AddChannel error, channel exists\n");
	}
	else{
		SP_Channel channel(new Channel(fd, io_watcher));
		channel_map_[fd] = channel;
	}
}

void Dispatcher::OnFdClosed(int fd){
	LogDebug("OnFdClosed %d\n", fd);
	ChannelMap::iterator iter = channel_map_.find(fd);
	if (iter != channel_map_.end()){
		//Channel* channel = iter->second;
		channel_map_.erase(fd);

		//delete channel;
		//channel = nullptr;
	}

		//let py to remove this socket
		//MessageQueue::getSingleton().MQ2S_Push_Close(uniqid);
}

void Dispatcher::InitEventFd(){
	//eventfd wakeup socket thread
	eventfd_ = netlib_eventfd();
	if (eventfd_ < 0)
	{
		LogError("netlib_socket error:%d\n",errno);
		exit(EXIT_FAILURE);
	}

	struct ev_io* efd_watcher = (struct ev_io*) malloc(sizeof(struct ev_io));
	ev_init(efd_watcher, eventfd_cb);
	AddEvent(efd_watcher, eventfd_, EV_READ);
}

void Dispatcher::InitTimer(){
	struct ev_timer* timeout_watcher = (struct ev_timer*) malloc(sizeof(struct ev_timer));
	ev_timer_init(timeout_watcher, init_timeout_cb, 1, 3); //1s后开始，3s的循环间隔
	ev_timer_start(loop_, timeout_watcher);
}

void Dispatcher::ConnectOtherServer(){
	for (auto itr = connector_map_.begin(); itr != connector_map_.end(); ++itr){
		SP_Connector connector = itr->second;
		if ( !connector->IsSuccess() ){
			//connect
			int conn_fd = connector->Fd();
			int ret = netlib_connect(conn_fd, connector->GetServerIp(), connector->GetServerPort());
			if (ret == 0){
				struct ev_io* conn_ev = (struct ev_io*) malloc(sizeof(struct ev_io));
				if (conn_ev == NULL)
				{
					LogError("malloc error in OnTryConnect\n");
					return;
				}

				ev_init(conn_ev, connector_cb);
				AddEvent(conn_ev, conn_fd, EV_READ);

				connector->SetIoWatcher(conn_ev);  //加入ev_io
				connector->SetSuccess(true);
				
				LogDebug("connect success:%s,%d\n", connector->GetServerIp(),connector->GetServerPort());
			}
			else{
				LogDebug("connect fail:%d,%s,%d\n",conn_fd, connector->GetServerIp(), connector->GetServerPort());
			}
		}
	}
}

void Dispatcher::accept_cb(struct ev_loop* loop, struct ev_io* watcher, int revents){
	int fd = watcher->fd;

	if (EV_ERROR & revents){
		//LogDebug("error event in accept\n");
		return;
	}
	printf("accept_cb \n");
	Dispatcher::getInstance().OnAccept(fd);
	//EpollServer::getSingleton().OnAccept(fd);
}

void Dispatcher::r_w_cb(struct ev_loop* loop, struct ev_io* watcher, int revents){
	int fd = watcher->fd;
	//LogDebug("r_w_cb %d,%d\n", fd, revents);
	if (EV_ERROR & revents){
		//LogError("error event in read or write\n");
		return;
	}

	if (EV_READ & revents){
		Dispatcher::getInstance().OnRead(fd, FD_TYPE_ACCEPT);
	}
	if (EV_WRITE & revents){
		Dispatcher::getInstance().OnWrite(fd, FD_TYPE_ACCEPT);
	}
}

void Dispatcher::eventfd_cb(struct ev_loop* loop, struct ev_io* watcher, int revents)
{
	int fd = watcher->fd;
	LogDebug("eventfd_cb %d,%d\n", fd, revents);
	if (EV_ERROR & revents)
	{
		LogError("error event in eventfd\n");
		return;
	}

	Dispatcher::getInstance().OnEventfd(fd);
}

void Dispatcher::connector_cb(struct ev_loop* loop, struct ev_io* watcher, int revents){
	int fd = watcher->fd;
	//LogDebug("connector_cb %d,%d\n", fd, revents);
	if (EV_ERROR & revents){
		//LogError("error event in read or write\n");
		return;
	}

	if (EV_READ & revents){
		Dispatcher::getInstance().OnRead(fd, FD_TYPE_CONNECT);
	}
	if (EV_WRITE & revents){
		Dispatcher::getInstance().OnWrite(fd, FD_TYPE_CONNECT);
	}
}

void Dispatcher::init_timeout_cb(struct ev_loop* loop, struct ev_timer* watcher, int revents){
	LogDebug("init_timeout_cb \n");
	Dispatcher::getInstance().OnTimer();
}

}
