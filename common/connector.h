/*
*作为client连接server的channel
*/

#include "channel.h"

namespace alpha{

class Connector : public Channel{

public:
	Connector(int fd, const char* server_ip, uint16_t port);
	~Connector();

	void SetIoWatcher(struct ev_io* io_watcher){io_watcher_ = io_watcher;}

	bool IsSuccess(){return success_;}

	void SetSuccess(bool success){success_ = success;}

	inline const char* GetServerIp(){return server_ip_;}
	inline uint16_t GetServerPort(){return port_;}

private:
	const char* server_ip_;
	uint16_t port_;

	bool success_;

};

}