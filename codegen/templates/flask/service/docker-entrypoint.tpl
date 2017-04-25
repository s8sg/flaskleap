#!/bin/bash

pid=0

# trap ctrl-c and call ctrl_c()
trap ctrl_c INT

function ctrl_c() {
	kill -2 $pid
	sleep 2
	exit 0
}

python /{{ service_name }}/server.py &
pid=$!

wait
