#include <stdio.h>
#include <ev.h> //ev库头文件

//定义一个ev_TYPE 的结构体
ev_io stdin_watcher;//定义一个stdin的观测者
ev_timer timeout_watcher;


//所有的watcher的回调函数都有相似的特点
//当stdin有可读的数据时，将会调用下面这个回调函数
static void stdin_cb(EV_P_ ev_io *w,int revents)
{
    puts("stdin ready");

    //每一次时间都必须用对应的停止函数，手动的停止其watcher
    ev_io_stop(EV_A_ w);
    //这将导致所有嵌套执行的ev_run停止监听
    ev_break(EV_A_ EVBREAK_ALL);
}

//这是一个回调函数，用于定时器回调
static void timeout_cb(EV_P_ ev_timer *w,int revents)
{
    puts("timeout");
    //这将导致最早运行的ev_run停止监听
    ev_break(EV_A_ EVBREAK_ONE);
}

int main(int argc,char **args)
{
    //使用一般默认的事件循环
    struct ev_loop *loop = EV_DEFAULT;

    //初始化一个I/O watcher，然后启动它
    ev_io_init(&stdin_watcher,stdin_cb,0,EV_READ);
    ev_io_start(loop,&stdin_watcher);

    //初始化一个定时器watcher，然后启动它，只有一次，没有重复的5.5秒定时
    ev_timer_init(&timeout_watcher,timeout_cb,5.5,0);
    ev_timer_start(loop,&timeout_watcher);

    //这里等待时间出发
    ev_run(loop,0);//0代表只循环一次

    //撤销监听退出程序
    return 0;
}