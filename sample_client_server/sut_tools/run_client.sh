#!/bin/bash

SRV=$1
PORT=$2

sleep 5
python3 /users/s2udayas/slicify/sample_client_server/socket_client.py $SRV $PORT