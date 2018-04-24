.PHONY: debug release clean rebuild cleantmp

CC = g++
CCFLAGS =-g -Wall

BIN_HOME = ../bin

LDFLAGS = -L/usr/local/lib

MOBILE_INCL = -I../common -I/usr/include/python3.6m
MOBILE_LIB = -lpthread -lev -lpython3.6m

CCFLAGS += $(MOBILE_INCL)
LDFLAGS += $(MOBILE_LIB)

CCFLAGS += -std=c++11

LIBS = ../common/libcommon.a

SOURCE  := $(wildcard *.c) $(wildcard *.cpp)
OBJS    := $(patsubst %.c,%.o,$(patsubst %.cpp,%.o,$(SOURCE)))

TARGET = $(BIN_HOME)/gate_server

all:  $(TARGET) cleantmp
$(BIN_HOME)/gate_server: $(OBJS) $(LIBS)
	$(CC) $(CCFLAGS) $(LDFLAGS) $^ -o $@
cleantmp:
	rm -f *.o
clean:
	rm -f *.o
	rm -f $(BIN_HOME)/gate_server
	
# make rule
%.o : %.c
	$(CC) $(CCFLAGS) -c $^ -o $@	

%.o : %.cpp
	$(CC) $(CCFLAGS) -c $^ -o $@