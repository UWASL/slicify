#!/bin/bash

echo "Running clients"
ssh node1 /users/s2udayas/slicify/sample_client_server/run_client.sh 10.10.1.3 5566 &

echo "Running servers"
ssh node2 /users/s2udayas/slicify/sample_client_server/run_server.sh 10.10.1.3 5566