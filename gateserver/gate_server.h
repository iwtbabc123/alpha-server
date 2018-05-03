#ifndef __GATE_SERVER_H__
#define __GATE_SERVER_H__

#include "util.h"
#include "gate_worker.h"
#include "cjson_helper.h"
using namespace alpha;

class GateServer{
public:
    GateServer();
    ~GateServer();

    void Start(const char* server_name, const char* config_file);

    void thread_socket(void* params);
    void thread_worker(void* params);

private:
    std::string server_name_;
    std::unique_ptr<GateWorker> worker_uptr_;
    std::unique_ptr<JsonHelper> json_uptr_;

};

#endif