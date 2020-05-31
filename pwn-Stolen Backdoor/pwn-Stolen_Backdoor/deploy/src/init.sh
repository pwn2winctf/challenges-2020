#!/bin/sh

chmod 700 /var/tmp /dev/shm
#hidepid=2

/home/manager/encoder > /dev/null &

su -m manager -c "/home/manager/daemon.py"
