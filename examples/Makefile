.PHONY: debug release clean rebuild cleantmp

CC = g++
CCFLAGS =-g -Wall

BIN_HOME = ../bin

LDFLAGS = -L/usr/local/lib

MOBILE_INCL = -I../common
MOBILE_LIB = -lpthread -lev

CCFLAGS += $(MOBILE_INCL)
LDFLAGS += $(MOBILE_LIB)

CCFLAGS += -std=c++11

LIBS = ../common/libcommon.a

TIMER_O = timer_test/timer_test.o

#THREAD_TEST_O= examples/thread_test/thread_test.o
#DISPATCHER_TEST_O= examples/dispatcher_test/dispatcher_test.o

TARGET = $(BIN_HOME)/timer_test #$(BIN_HOME)/dispatcher_test \
			$(BIN_HOME)/gate_server

all:  $(TARGET) cleantmp
$(BIN_HOME)/timer_test: $(TIMER_O) $(LIBS)
	$(CC) $(CCFLAGS) $^ -o $@ $(LDFLAGS)
cleantmp:
	rm -f *.o
clean:
	rm -f *.o
	rm -f $(BIN_HOME)/timer_test
	
# make rule
%.o : %.c
	$(CC) $(CCFLAGS) -c $^ -o $@	

%.o : %.cpp
	$(CC) $(CCFLAGS) -c $^ -o $@
