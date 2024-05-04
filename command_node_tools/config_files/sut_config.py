import os
"""
    File containing SUT configuration information
    ** TO BE FILLED IN BY DEVELOPER **    
"""

sut_tools_dir = "sut_tools"
sut_dir = "/users/s2udayas/slicify/sample_client_server/"
sut_tools_full_path = os.path.join(sut_dir, sut_tools_dir)

sut_logs_path = "sut_logs/"

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
    "3WayComms" : os.path.join(sut_tools_full_path, "3WayComms.sh")
}

# Post unit-test clean up commands
clean_up_commands = {

}

# Test result verification commands
verification_commands = {

}
    
# Path to application logs
log_collection_commands = {
    
}


