#ifndef __ALPHA_THREAD_SOCKET_H__
#define __ALPHA_THREAD_SOCKET_H__

namespace alpha{

class ThreadSocket{

public:
	ThreadSocket();
	~ThreadSocket();

	void Start(int port);
};

}

#endif