#ifndef __ALPHA_DISPATCHER_H__
#define __ALPHA_DISPATCHER_H__

#include <ev.h>
#include <map>
#include "util.h"
#include "channel.h"
//#include "connector.h"

namespace alpha{

//typedef std::shared_ptr<Channel> SP_Channel;
typedef std::unique_ptr<Channel> UP_Channel;

class Dispatcher{
public:
    static Dispatcher& getInstance(){
		static Dispatcher instance;
		return instance;
	}

    void StartServer(uint16_t port);

    void ConnectIpPort(const char* ip, uint16_t port);

    void OnAccept(int fd);
    void OnRead(int fd, int fd_type);
    void OnWrite(int fd, int fd_type);
    void OnEventfd(int fd);
    void OnConnect(int fd, int revents);
public:
    int Eventfd(){return eventfd_;}

public:
    //接受客户端连接
    static void accept_cb(struct ev_loop* loop, struct ev_io* watcher, int revents);
    //接受客户端读写
    static void r_w_cb(struct ev_loop* loop, struct ev_io* watcher, int revents);
    //接受worker线程eventfd,处理消息队列
    static void eventfd_cb(struct ev_loop* loop, struct ev_io* watcher, int revents);
    //连接其它server的socket的读写及连接事件
    static void connector_cb(struct ev_loop* loop, struct ev_io* watcher, int revents);

private:
    Dispatcher();

    ~Dispatcher();

private:
	int AddEvent(struct ev_io* io_watcher, int fd, short events);

	int UpdateEvent(int fd, short events, UP_Channel* channel);

	void RemoveEvent(int fd, int fd_type);

    UP_Channel* GetChannel(int fd, int fd_type);

    void AddChannel(int fd, int fd_type, ev_io* io_watcher);

    void OnFdClosed(int fd, int fd_type);  //RemoveChannel

private:
    void InitEventFd();

private:
    struct ev_loop* loop_;
    bool running_;

    int eventfd_;
    typedef std::map<int, UP_Channel> ChannelMap;
    ChannelMap channel_map_;
    ChannelMap connector_map_;

private:
    Dispatcher::ChannelMap& _GetChannelMap(int fd_type);

};

}

#endif