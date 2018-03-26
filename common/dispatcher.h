#ifndef __ALPHA_DISPATCHER_H__
#define __ALPHA_DISPATCHER_H__

#include <ev.h>
#include "util.h"

namespace alpha{

class Dispatcher final{
public:
    Dispatcher();

    ~Dispatcher();

private:
    struct ev_loop* m_ev_loop;
    bool m_running;
    

}

}

#endif