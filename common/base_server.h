#ifndef __ALPHA_BASE_SERVER_H__
#define __ALPHA_BASE_SERVER_H__

#include <pthread.h>
#include "config_reader.h"
#include "cjson_helper.h"
#include "message_queue.h"

namespace alpha{

class BaseServer{
public:

	BaseServer();

	virtual ~BaseServer();

	virtual void LoadConfig(const char* server_name, const char* config_file);

	struct message_queue* MessageDispatch();

protected:
	void CreateThread(pthread_t* thread, void*(cb)(void*), void* arg);

private:
	std::unique_ptr<JsonHelper> m_json;

	MessageQueue mq_;

};

}

#endif