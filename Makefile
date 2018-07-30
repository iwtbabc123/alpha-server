
all:
	cd common; make;
	cd server; make;
clean:
	cd common; make clean;
	cd server; make clean;
