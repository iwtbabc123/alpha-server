#ifndef __GATE_SERVER_H__
#define __GATE_SERVER_H__

#include "base_server.h"

using namespace alpha;

class GateServer:public BaseServer{
public:
    GateServer();
    ~GateServer();

    void Start(const char* server_name, const char* config_file);

    void thread_socket();
    void thread_worker();
};

#endif