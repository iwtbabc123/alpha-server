#include <Python.h>
#include "gate_server.h"
#include "thread.h"

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


GateServer::GateServer():BaseServer(){
	Py_InitModule("alphaEngine", AlphaMethods);
}

GateServer::~GateServer(){

}

void GateServer::Start(const char* server_name, const char* config_file){
	LoadConfig(server_name, config_file);

	auto f_socket = std::bind(this->thread_socket);

	std::unique_ptr<Thread> up_socket = new Thread(f_socket);
	up_socket->start();

	auto f_worker = std::bind(this->thread_worker);

	std::unique_ptr<Thread> up_worker = new Thread(f_worker);

}

void GateServer::thread_socket(){

}

void GateServer::thread_worker(){
	
}