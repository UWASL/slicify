#!/bin/bash

# echo "Running clients"
ssh node1 /users/s2udayas/slicify/sample_client_server/sut_tools/run_client.sh 10.10.1.3 5567 &
ssh node2 /users/s2udayas/slicify/sample_client_server/sut_tools/run_client.sh 10.10.1.4 5568 &
ssh node3 /users/s2udayas/slicify/sample_client_server/sut_tools/run_client.sh 10.10.1.2 5566 &

# echo "Running servers"
ssh node1 /users/s2udayas/slicify/sample_client_server/sut_tools/run_server.sh 10.10.1.2 5566 &
ssh node2 /users/s2udayas/slicify/sample_client_server/sut_tools/run_server.sh 10.10.1.3 5567 &
ssh node3 /users/s2udayas/slicify/sample_client_server/sut_tools/run_server.sh 10.10.1.4 5568

echo "3WayComms test execution complete"