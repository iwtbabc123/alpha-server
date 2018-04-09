# Makefile, 去掉 .so,直接打进,如果想生成 .so,可以使用 common/makefile

CC = g++
CCFLAGS =-g

BIN_HOME = ./bin

LDFLAGS = -L/usr/local/lib

MOBILE_INCL = -I./common -I/usr/include/python3.6m
MOBILE_LIB = -lpthread -lev -lpython3.6m

CCFLAGS += $(MOBILE_INCL)
LDFLAGS += $(MOBILE_LIB)

CCFLAGS += -std=c++11

#-lprotobuf
USER_LDFLAGS = 

COMMON_O = common/util.o common/logger.o common/thread.o common/net_util.o \
			common/message_queue.o common/channel.o common/dispatcher.o

GATE_O = gateserver/gate_worker.o gateserver/gate_server.o gateserver/main.o

#DB_O= dbserver/db_server.o dbserver/db_conn.o dbserver/db_worker.o dbserver/main.o

#TARGET = $(BIN_HOME)/gameserver $(BIN_HOME)/dbserver

THREAD_TEST_O= examples/thread_test/thread_test.o
DISPATCHER_TEST_O= examples/dispatcher_test/dispatcher_test.o

TARGET = $(BIN_HOME)/thread_test $(BIN_HOME)/dispatcher_test \
			$(BIN_HOME)/gate_server

all:  $(TARGET)
$(BIN_HOME)/gate_server: $(COMMON_O) $(GATE_O)
	$(CC) $(CCFLAGS) $(LDFLAGS) $(USER_LDFLAGS) $^ -o $@
$(BIN_HOME)/thread_test: $(COMMON_O) $(THREAD_TEST_O)
	$(CC) $(CCFLAGS) $(LDFLAGS) $(USER_LDFLAGS) $^ -o $@
$(BIN_HOME)/dispatcher_test: $(COMMON_O) $(DISPATCHER_TEST_O)
	$(CC) $(CCFLAGS) $(LDFLAGS) $(USER_LDFLAGS) $^ -o $@
clean:
	rm -f common/*.o common/*.so common/*.a
	rm -f examples/thread_test/*.o $(BIN_HOME)/thread_test
	
# make rule
%.o : %.c
	$(CC) $(CCFLAGS) -c $^ -o $@	

%.o : %.cpp
	$(CC) $(CCFLAGS) -c $^ -o $@