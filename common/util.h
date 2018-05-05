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

//to worker fd
#define FD_TYPE_CONN	1
#define FD_TYPE_READ	2

//to socket fd
#define FD_TYPE_CLIENT	11
#define FD_TYPE_SERVER	12
#define FD_TYPE_TIMER	13

}

#endif