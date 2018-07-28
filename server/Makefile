.PHONY: debug release clean rebuild cleantmp

CC = g++
CCFLAGS =-g -Wall

BIN_HOME = ../bin

LDFLAGS = -L/usr/local/lib

MOBILE_INCL = -I../common -I/usr/include/python3.5m
MOBILE_LIB = -lpthread -lev -lpython3.5m

CCFLAGS += $(MOBILE_INCL)
LDFLAGS += $(MOBILE_LIB)

CCFLAGS += -std=c++11

LIBS = ../common/libcommon.a

SOURCE  := $(wildcard *.c) $(wildcard *.cpp)
OBJS    := $(patsubst %.c,%.o,$(patsubst %.cpp,%.o,$(SOURCE)))

TARGET = $(BIN_HOME)/server

all:  $(TARGET) cleantmp
$(BIN_HOME)/server: $(OBJS) $(LIBS)
	$(CC) $(CCFLAGS) $^ -o $@ $(LDFLAGS)
cleantmp:
	rm -f *.o
clean:
	rm -f *.o
	rm -f $(BIN_HOME)/server
	
# make rule
%.o : %.c
	$(CC) $(CCFLAGS) -c $^ -o $@	

%.o : %.cpp
	$(CC) $(CCFLAGS) -c $^ -o $@
