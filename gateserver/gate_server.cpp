//#include <Python.h>
#include "gate_server.h"
#include "util.h"
/*
static PyObject*
call_client(PyObject* self, PyObject* args)
{
	//LogDebug("py->cpp call_client\n");

	int uniqid;
	int command_id;  //用uint16_t会读不到数据
	int sub_id;
	char* str;
	if (!PyArg_ParseTuple(args, "iiis", &uniqid, &command_id, &sub_id, &str))
		Py_RETURN_NONE;
	MessageQueue::getSingleton().MQ2C_Push(uniqid, command_id, sub_id, str);
	
	Py_RETURN_NONE;
}

static PyMethodDef PlutoMethods[] = {
    {"call_client", call_client, METH_VARARGS, "Call client method"},
    //{"broad_cast", broad_cast, METH_VARARGS, "broadcast method"},
    //{"add_timer", add_timer, METH_VARARGS, "add_timer method"},
    //{"on_load", on_load, METH_VARARGS, "on_load method"},
    //{"on_save", on_save, METH_VARARGS, "on_save method"},
    //{"log_info", log_info, METH_VARARGS, "log info"},
    //{"add_repeat_timer", add_repeat_timer, METH_VARARGS, "add_repeat_timer method"},
    {NULL, NULL, 0, NULL}
};
*/

GateServer::GateServer():BaseServer(){
	//Py_InitModule("alphaEngine", AlphaMethods);
}

GateServer::~GateServer(){

}

void GateServer::Start(const char* server_name, const char* config_file){
	printf("main thread %u\n", (unsigned int)pthread_self());
	//LoadConfig(server_name, config_file);

	void* params = nullptr;
	auto func_socket = std::bind(&GateServer::thread_socket, this, std::placeholders::_1);

	std::unique_ptr<Thread> uni_ptr1(new Thread(func_socket));
	uni_ptr1->start(params);

	auto func_worker = std::bind(&GateServer::thread_worker, this, std::placeholders::_1);

	std::unique_ptr<Thread> uni_ptr2(new Thread(func_worker));
	uni_ptr2->start(params);

	uni_ptr2->join();

}

void GateServer::thread_socket(void* params){
	printf("new thread_socket %u\n", (unsigned int)pthread_self());
}

void GateServer::thread_worker(void* params){
	printf("new thread_worker %u\n", (unsigned int)pthread_self());
}