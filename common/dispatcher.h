#ifndef __ALPHA_DISPATCHER_H__
#define __ALPHA_DISPATCHER_H__

#include <ev.h>
#include <map>
#include "util.h"
#include "channel.h"
#include "connector.h"

namespace alpha{

typedef std::shared_ptr<Channel> SP_Channel;
typedef std::shared_ptr<Connector> SP_Connector;

class Dispatcher{
public:
    static Dispatcher& getInstance(){
		static Dispatcher instance;
		return instance;
	}

    void StartServer(uint16_t port);
    //连接其它server,为了保证重连，需要逻辑层做定时重连相关功能
    void ConnectIpPort(const char* ip, uint16_t port);

    void OnAccept(int fd);
    void OnRead(int fd, int fd_type);
    void OnWrite(int fd, int fd_type);
    void OnEventfd(int fd);
    void OnTimer();
public:
    int Eventfd(){return eventfd_;}

public:
    static void accept_cb(struct ev_loop* loop, struct ev_io* watcher, int revents);
    static void r_w_cb(struct ev_loop* loop, struct ev_io* watcher, int revents);
    static void eventfd_cb(struct ev_loop* loop, struct ev_io* watcher, int revents);
    //连接其它server的socket
    static void connector_cb(struct ev_loop* loop, struct ev_io* watcher, int revents);
    static void init_timeout_cb(struct ev_loop* loop, struct ev_timer* watcher, int revents);

private:
    Dispatcher();

    ~Dispatcher();

private:
	int AddEvent(struct ev_io* io_watcher, int fd, short events);

	int UpdateEvent(int fd, short events, SP_Channel channel);

	void RemoveEvent(int fd);

    SP_Channel GetChannel(int fd);

    void AddChannel(ev_io* io_watcher, int fd);

    void OnFdClosed(int fd);  //RemoveChannel

private:
    void InitEventFd();
    void InitTimer();
    void ConnectOtherServer();

private:
    struct ev_loop* loop_;
    bool running_;

    int eventfd_;
    typedef std::map<int, SP_Channel> ChannelMap;
    typedef std::map<int, SP_Connector> ConnectorMap;
    ChannelMap channel_map_;
    ConnectorMap connector_map_;

};

}

#endif