#ifndef __ALPHA_DISPATCHER_H__
#define __ALPHA_DISPATCHER_H__

#include <ev.h>
#include <map>
#include "util.h"

namespace alpha{

class Channel;
class Dispatcher{
public:
    static Dispatcher& getInstance(){
		static Dispatcher instance;
		return instance;
	}

    void StartServer(uint16_t port);

    void OnAccept(int fd);
    void OnRead(int fd);

public:
    static void accept_cb(struct ev_loop* loop, struct ev_io* watcher, int revents);
    static void r_w_cb(struct ev_loop* loop, struct ev_io* watcher, int revents);

private:
    Dispatcher();

    ~Dispatcher();

private:
	int AddEvent(struct ev_io* io_watcher, int fd, short events);

	//int UpdateEvent(int fd, short events, Channel* channel);

	void RemoveEvent(int fd);

    Channel* GetChannel(int fd);

    void AddChannel(ev_io* io_watcher, int fd);

    void OnFdClosed(int fd);  //RemoveChannel

private:
    struct ev_loop* loop_;
    bool running_;
    
    typedef std::map<int, Channel*> ChannelMap;
    ChannelMap channel_map_;

};

}

#endif