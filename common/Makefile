#common

CC = g++
AR = ar cru
CCFLAGS = -Wall -g -fPIC
SOFLAGS = -shared

LDFLAGS = -L/usr/local/lib

ALPHA_INCL =
ALPHA_LIB = -lev

CCFLAGS += $(ALPHA_INCL)
LDFLAGS += $(ALPHA_LIB)

#-lprotobuf
USER_LDFLAGS = 

LIBOBJS = thread.o

TARGET = libcommon.so libcommon.a

all:  $(TARGET)

libcommon.so: $(LIBOBJS)
	$(CC) $(SOFLAGS) $(LDFLAGS) $(USER_LDFLAGS) $^ -o $@
libcommon.a: $(LIBOBJS)
	$(AR) $@ $^

clean:
	rm -f *.o *.so *.a
	
# make rule
%.o : %.c
	$(CC) $(CCFLAGS) -c $^ -o $@	

%.o : %.cpp
	$(CC) $(CCFLAGS) -c $^ -o $@