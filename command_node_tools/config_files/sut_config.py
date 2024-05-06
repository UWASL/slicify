import os
"""
    File containing SUT configuration information
    ** TO BE FILLED IN BY DEVELOPER **    
"""

sut_tools_dir = "sut_tools"
sut_dir = "/users/s2udayas/slicify/sample_client_server/"

# This is where the SUT logs information by default
sut_logs_dir = "sut_logs/"

# This is where the final logs of tests under partitions will be stored
sut_test_logs_root_dir = "sut_test_logs/"

sut_tools_full_path = os.path.join(sut_dir, sut_tools_dir)
sut_test_logs_path = os.path.join(sut_dir, sut_test_logs_root_dir)
sut_logs_path = os.path.join(sut_dir, sut_logs_dir)


# Please note that all commands are processed serially
# Commands to setup SUT and its dependencies on each cluster-node
# Key = Node IP, Value = Run command
setup_commands = {
    "node1" : os.path.join(sut_tools_full_path, "install_sut.sh"),
    "node2" : os.path.join(sut_tools_full_path, "install_sut.sh"),
    "node3" : os.path.join(sut_tools_full_path, "install_sut.sh")
}

# Commands to run test cases 
# Key = Test case name, Value = Run command
run_program_commands = {
    "3WayComms" : os.path.join(sut_tools_full_path, "3WayComms.sh"),
    "1WayComms" : os.path.join(sut_tools_full_path, "1WayComms.sh")
}

kill_program_commands = {
    "node1" : "killall python3",
    "node2" : "killall python3",
    "node3" : "killall python3"
}

# Post unit-test clean up commands
clean_up_commands = {
    "node1": "rm -f " + os.path.join(sut_logs_path, "*.txt"),
    "node2": "rm -f " + os.path.join(sut_logs_path, "*.txt"),
    "node3": "rm -f " + os.path.join(sut_logs_path, "*.txt")
}

# Test result verification commands
verification_commands = {

}
    
# Path to application logs
log_collection_commands = {
    
}


