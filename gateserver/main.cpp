#include "gate_server.h"
#include "util.h"

using namespace alpha;

const char* config_file = "config.json";

void siginthandler(int param)
{
  printf("User pressed Ctrl+C\n");
  exit(1);
}

int main(int argc, char* argv[]){
    signal(SIGINT, siginthandler);
    signal(SIGPIPE, SIG_IGN);

    if(argc < 2){
        printf("arg num is less than 2\n");
        return -1;
    }

    if(strncmp(argv[1], "--", 2) != 0){
        printf("arg should start with--\n");
        return -1;
    }

    const char* server_name = argv[1]+2;
    GateServer server;
    server.Start(server_name, config_file);
}