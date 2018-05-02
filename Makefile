
all:
	cd common; make;
	cd gateserver; make;
clean:
	cd common; make clean;
	cd gateserver; make clean;
