#ifndef __SERVER_H__
#define __SERVER_H__

#include "util.h"
#include "cjson_helper.h"
#include "worker_thread.h"

using namespace alpha;

class Server{
public:
    Server();
    ~Server();

    void Start(const char* server_name, const char* config_file);

    void thread_socket(void* params);
    void thread_worker(void* params);
    void thread_timer(void* params);

private:
    std::string server_name_;
    std::unique_ptr<WorkerThread> worker_uptr_;
    std::unique_ptr<JsonHelper> json_uptr_;

};

#endif