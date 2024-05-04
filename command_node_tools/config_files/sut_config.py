"""
    File containing SUT configuration information
    ** TO BE FILLED IN BY DEVELOPER **    
"""

sut_tools_dir = "sut_tools"
sut_dir = "/users/s2udayas/slicify/sample_client_server/"

sut_logs_path = "sut_logs/"

# Please note that all commands are processed serially
# Commands to setup SUT and its dependencies on each cluster-node
setup_commands = {
    "node1" : "/users/s2udayas/slicify/sample_client_server/sut_tools/install_sut.sh",
    "node2" : "/users/s2udayas/slicify/sample_client_server/sut_tools/install_sut.sh",
    "node3" : "/users/s2udayas/slicify/sample_client_server/sut_tools/install_sut.sh"
}

# Commands to run test cases 
run_program_commands = {

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


