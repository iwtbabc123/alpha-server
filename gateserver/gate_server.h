#ifndef __GATE_SERVER_H__
#define __GATE_SERVER_H__

#include "util.h"
using namespace alpha;

class GateServer{
public:
    GateServer();
    ~GateServer();

    void Start(const char* server_name, const char* config_file);

    void thread_socket(void* params);
    void thread_worker(void* params);
};

#endif