#include "timer.h"

#include <sys/time.h> 
#include <time.h>
#include <stdio.h>
#include <stdlib.h>

#define USEC_PER_SEC 1000000
#define MSEC_PER_SEC 1000

#define evutil_timercmp(tvp, uvp, cmp)  \
	(((tvp)->tv_sec == (uvp)->tv_sec) ? \
	((tvp)->tv_usec cmp (uvp)->tv_usec) : \
	((tvp)->tv_sec cmp (uvp)->tv_sec))

#define evutil_timersub(tvp, uvp, vvp)  \
do {\
	(vvp)->tv_sec = (tvp)->tv_sec - (uvp)->tv_sec; \
	(vvp)->tv_usec = (tvp)->tv_usec - (uvp)->tv_usec; \
	if ((vvp)->tv_usec < 0) { \
		(vvp)->tv_sec--; \
		(vvp)->tv_usec += USEC_PER_SEC; \
	}   \
} while (0)

#define evutil_timeradd(tvp, uvp, vvp)  \
do {\
	(vvp)->tv_sec = (tvp)->tv_sec + (uvp)->tv_sec; \
	(vvp)->tv_usec = (tvp)->tv_usec + (uvp)->tv_usec;   \
	if ((vvp)->tv_usec >= USEC_PER_SEC) {  \
	(vvp)->tv_sec++; \
	(vvp)->tv_usec -= USEC_PER_SEC;   \
	}   \
} while (0)

namespace alpha{

struct event{
	unsigned int min_heap_idx; /* for managing timeouts */
	unsigned int timer_id;
	struct timeval ev_interval;
	struct timeval ev_timeout;
	int ev_num;

	void (*ev_callback)(void *arg);
	void *ev_arg;

	int ev_res; /* result passed to event callback */
	bool ev_flags;
};

/***构造函数  ***************/
static inline void min_heap_ctor(min_heap_t* s);
/***析构函数  ***************/
static inline void min_heap_dtor(min_heap_t* s);
/***初始化函数  ***************/
static inline void min_heap_elem_init(struct event* e);
/****比较函数***************/
static inline int min_heap_elem_greater(struct event *a, struct event *b);

static inline bool min_heap_empty(min_heap_t* s);

static inline unsigned int min_heap_size(min_heap_t* s);
/****返回栈顶元素************/
static inline struct event* min_heap_top(min_heap_t* s);
/****调整定时器的大小*********/
static inline int min_heap_reserve(min_heap_t* s, unsigned n);
/****放入数据*************/
static inline int min_heap_push(min_heap_t* s, struct event* e);
/****取得最后上面的数据******/
static inline struct event* min_heap_pop(min_heap_t* s);
/****消除一个定时器元素*******/
static inline int min_heap_erase(min_heap_t* s, struct event* e);
/****向上调整 ************/
static inline void min_heap_shift_up_(min_heap_t* s, unsigned hole_index, struct event* e);
/****向下调整************/
static inline void min_heap_shift_down_(min_heap_t* s, unsigned hole_index, struct event* e);

static inline void gettime(struct timeval *tm);

Timer::Timer():timer_id_(0){
	min_heap_ctor(&min_heap_);
}

Timer::~Timer(){
	for (unsigned int i = 0; i < min_heap_.n; i++){
		free(min_heap_.p[i]);
	}
	min_heap_dtor(&min_heap_);
}

unsigned int Timer::timer_add(int interval, void(*fun)(void*), void *arg,bool forever /* = true */, int num /* =  1 */)
{
	struct event * ev = (struct event*) malloc(sizeof(struct event));
	min_heap_elem_init(ev);
	if (nullptr == ev)
		return 0;
	struct timeval now;
	gettime(&now);
	ev->ev_interval.tv_sec = interval / MSEC_PER_SEC;
	ev->ev_interval.tv_usec = (interval % MSEC_PER_SEC) * MSEC_PER_SEC;
	evutil_timeradd(&now, &(ev->ev_interval), &(ev->ev_timeout));
	ev->ev_flags = forever;
	ev->ev_callback = fun;
	ev->ev_arg = arg;
	ev->ev_num = num;
	ev->timer_id = timer_id_++;
	min_heap_push(&min_heap_, ev);

	return ev->timer_id;
}

bool Timer::timer_remove(unsigned int timer_id)
{
	for (unsigned int i = 0; i < min_heap_.n; i++)
	{
		if (timer_id == min_heap_.p[i]->timer_id)
		{
			struct event * e = min_heap_.p[i];
			min_heap_erase(&min_heap_, min_heap_.p[i]);
			free(e);
			return true;
		}
	}
	return false;
}

int Timer::timer_process()
{
	struct event *event;
	struct timeval now;
	while ((event = min_heap_top(&min_heap_)) != nullptr)
	{
		gettime(&now);
		if (evutil_timercmp(&now, &(event->ev_timeout), < )){
			break;
		}
		min_heap_pop(&min_heap_);
		event->ev_callback(event->ev_arg);
		if (event->ev_flags == true || (event->ev_flags == false && --event->ev_num > 0))
		{
			evutil_timeradd(&(event->ev_timeout), &(event->ev_interval), &(event->ev_timeout));
			min_heap_push(&min_heap_, event);
		}
		else
		{
			free(event);
		}
	}

	return 0;
}

void gettime(struct timeval *tm)
{
	gettimeofday(tm, NULL);
}

int min_heap_elem_greater(struct event *a, struct event *b)
{
	return evutil_timercmp(&a->ev_timeout, &b->ev_timeout, >);
}

void min_heap_ctor(min_heap_t* s)
{
	s->p = 0;
	s->n = 0;
	s->a = 0;
}

void min_heap_dtor(min_heap_t* s)
{
	if (s->p)
	free(s->p);
}

void min_heap_elem_init(struct event* e)
{
	e->min_heap_idx = -1;
}

bool min_heap_empty(min_heap_t* s)
{
	return 0 == s->n;
}

unsigned int min_heap_size(min_heap_t* s)
{
	return s->n;
}

struct event* min_heap_top(min_heap_t* s)
{
	return s->n ? *s->p : nullptr;
}

int min_heap_push(min_heap_t* s, struct event* e)
{
	if (min_heap_reserve(s, s->n + 1)){
		return -1;
	}
	min_heap_shift_up_(s, s->n++, e);
	return 0;
}

struct event* min_heap_pop(min_heap_t* s)
{
	if (s->n)
	{
		struct event* e = *s->p;
		min_heap_shift_down_(s, 0u, s->p[--s->n]);
		e->min_heap_idx = -1;
		return e;
	}
	return 0;
}

int min_heap_erase(min_heap_t* s, struct event* e)
{
	if (((unsigned int) -1) != e->min_heap_idx)
	{
		struct event *last = s->p[--s->n];
		unsigned parent = (e->min_heap_idx - 1) / 2;
		/* we replace e with the last element in the heap.  We might need to  
		shift it upward if it is less than its parent, or downward if it is  
		greater than one or both its children. Since the children are known  
		to be less than the parent, it can't need to shift both up and  
		down. */
		if (e->min_heap_idx > 0 && min_heap_elem_greater(s->p[parent], last))
		min_heap_shift_up_(s, e->min_heap_idx, last);
		else
		min_heap_shift_down_(s, e->min_heap_idx, last);
		e->min_heap_idx = -1;
		return 0;
	}
	return -1;
}

int min_heap_reserve(min_heap_t* s, unsigned n)
{
	if (s->a < n)
	{
		struct event** p;
		unsigned a = s->a ? s->a * 2 : 8;
		if (a < n)
		a = n;
		if (!(p = (struct event**) realloc(s->p, a * sizeof *p)))
		return -1;
		s->p = p;
		s->a = a;
	}
	return 0;
}

void min_heap_shift_up_(min_heap_t* s, unsigned hole_index, struct event* e)
{
	unsigned parent = (hole_index - 1) / 2;
	while (hole_index && min_heap_elem_greater(s->p[parent], e))
	{
		(s->p[hole_index] = s->p[parent])->min_heap_idx = hole_index;
		hole_index = parent;
		parent = (hole_index - 1) / 2;
	}
	(s->p[hole_index] = e)->min_heap_idx = hole_index;
}

void min_heap_shift_down_(min_heap_t* s, unsigned hole_index, struct event* e)
{
	unsigned min_child = 2 * (hole_index + 1);
	while (min_child <= s->n)
	{
		min_child -= min_child == s->n
		|| min_heap_elem_greater(s->p[min_child], s->p[min_child - 1]);
		if (!(min_heap_elem_greater(e, s->p[min_child])))
			break;
		(s->p[hole_index] = s->p[min_child])->min_heap_idx = hole_index;
		hole_index = min_child;
		min_child = 2 * (hole_index + 1);
	}
	min_heap_shift_up_(s, hole_index, e);
}
} /* namespace alpha */