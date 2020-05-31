all:
	gcc -c -Wall emojinet.c -fpic -s
	gcc -shared -o libemojinet.so emojinet.o -s
	strip --strip-all --discard-all libemojinet.so
	gcc -Wall -o encoder encoder.c -lemojinet -s
	sudo cp libemojinet.so /lib/x86_64-linux-gnu/
	cp libemojinet.so ../../deploy/src/
	cp encoder ../../deploy/src/
	rm *.o
