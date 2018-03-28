#ifndef __ALPHA_DISPATCHER_H__
#define __ALPHA_DISPATCHER_H__

#include <ev.h>
#include "util.h"

namespace alpha{

class Dispatcher{
public:
    Dispatcher();

    ~Dispatcher();

    void StartServer(uint16_t port);

public:
    static void accept_cb(struct ev_loop* loop, struct ev_io* watcher, int revents);

private:
	int AddEvent(struct ev_io* io_watcher, int fd, short events);

	//int UpdateEvent(int fd, short events, Channel* channel);

	//void RemoveEvent(int fd, Channel* channel);

private:
    struct ev_loop* loop_;
    bool running_;
    

};

}

#endif