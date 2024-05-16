#!/bin/bash

# echo "Running clients"
ssh node3 /users/s2udayas/slicify/sample_client_server/sut_tools/run_client.sh 10.10.1.2 5566 &

# echo "Running servers"
ssh node1 /users/s2udayas/slicify/sample_client_server/sut_tools/run_server.sh 10.10.1.2 5566

echo "1WayComms test execution complete"