# Makefile, 去掉 .so,直接打进,如果想生成 .so,可以使用 common/makefile

CC = g++
CCFLAGS =-g

BIN_HOME = ./bin

LDFLAGS = -L/usr/local/lib

MOBILE_INCL = -I./common
MOBILE_LIB = -lpthread -lev

CCFLAGS += $(MOBILE_INCL)
LDFLAGS += $(MOBILE_LIB)

CCFLAGS += -std=c++11

#-lprotobuf
USER_LDFLAGS = 

COMMON_O = common/util.o common/logger.o common/thread.o common/net_util.o common/dispatcher.o

#GAME_O= gameserver/game_server.o gameserver/game_cpp2py.o gameserver/game_py2cpp.o gameserver/game_worker.o gameserver/main.o

#DB_O= dbserver/db_server.o dbserver/db_conn.o dbserver/db_worker.o dbserver/main.o

#TARGET = $(BIN_HOME)/gameserver $(BIN_HOME)/dbserver

THREAD_TEST_O= examples/thread_test/thread_test.o
DISPATCHER_TEST_O= examples/dispatcher_test/dispatcher_test.o

TARGET = $(BIN_HOME)/thread_test $(BIN_HOME)/dispatcher_test

all:  $(TARGET)

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