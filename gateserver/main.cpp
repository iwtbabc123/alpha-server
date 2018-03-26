#include "gate_server.h"
#include "util.h"

using namespace alpha;

int main(int argc, char* argv[]){
    singal(SIGPIPE, SIG_IGN);

    if(argc < 2){
        printf("arg num is less than 2\n");
    }

    if(strncmp(argv[1], "--", 2) != 0){
        printf("arg should start with--\n");
    }

    char* server_name = argv[1]+2;
    GateServer server;
    server.Start(server_name, "config.json");
}