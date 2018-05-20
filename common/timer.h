#ifndef __ALPHA_TIMER_H__
#define __ALPHA_TIMER_H__

#include <functional>
#include <pthread.h>

namespace alpha{

typedef std::function<void (int time_id)> TimerFunc;

struct event;

typedef struct min_heap{
    struct event** p;
    unsigned int n, a;
} min_heap_t;

class Timer{

public:
    static Timer& getInstance(){
		static Timer instance;
		return instance;
	}

public:
    Timer();
    virtual ~Timer();
    /*
    * delay: 延迟ms后开始执行
    * func: 完成后执行的func
    * interval: if interval != 0 指每隔interval执行一次
    * */
    unsigned int timer_add(int delay, TimerFunc func,  int interval = 0);
    /*
    * 强制删除某定时器
    * */
    bool timer_remove(unsigned int timer_id);
    /*
    * 定时器的循环处理函数，由定时器的拥有者进行循环调用。它的最小时间间隔决定了定时器的精度。  
    * */
    int timer_process();

    void set_common_func(TimerFunc func){
        func_ = std::move(func);
    }

private:
    void Timer_Lock();

	void Timer_Unlock();

private:
    struct min_heap min_heap_;
    unsigned int timer_id_;

    pthread_mutex_t timer_lock_;

    TimerFunc func_;  //设置通用的回调函数
};

} /* namespace alpha */
#endif /* __ALPHA_TIMER_H__ */  
