
#include "thread.h"

using namespace alpha;

class Thread_test{

public:
	Thread_test();

	void start();

	void new_thread_test(void* params);

private:
	int int_val_;
};
