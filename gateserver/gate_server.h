#ifndef __GATE_SERVER_H__
#define __GATE_SERVER_H__

#include "util.h"
#include "message_queue.h"
#include "gate_worker.h"
using namespace alpha;

class GateServer{
public:
    GateServer();
    ~GateServer();

    void Start(const char* server_name, const char* config_file);

    void thread_socket(void* params);
    void thread_worker(void* params);

private:
    std::unique_ptr<GateWorker> worker_uptr_;  //TODO,是否在thread_worker里面声明就行

};

#endif