#ifndef __ALPHA_UTIL_H__
#define __ALPHA_UTIL_H__

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <signal.h>
#include <memory>
#include <functional>
#include <string>

namespace alpha{

#define MAX_LOG_BUFF_SIZE 1024
#define READ_BUF_SIZE	1024

#define LOG_NONE		0x00  //LOG_NONE
#define LOG_DEBUG		0x01  //LOG_DEBUG
#define LOG_INFO		0x02  //LOG_INFO
#define LOG_WARNING		0x04  //LOG_WARNING
#define LOG_ERROR		0x08  //LOG_ERROR
#define LOG_ALL			0xff  //LOG_ALL

//fd type
#define FD_TYPE_ACCEPT		1  //accept client socket
#define FD_TYPE_CLIENT		2  //read or write client socket
#define FD_TYPE_CLOSE		3  //close socket
#define FD_TYPE_TIMER		4
#define FD_TYPE_SERVER		5  //read or write server socket
#define FD_TYPE_CONNECT		6  //connect to server
}

#endif
