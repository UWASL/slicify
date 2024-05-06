import os, time
import subprocess
import config_files.slicify_config as slicify_config
import config_files.sut_config as sut_config

sut_setup_commands = sut_config.setup_commands
sut_tests = sut_config.run_program_commands
sut_verify = sut_config.verification_commands
sut_log_collect_commands = sut_config.log_collection_commands
sut_cleanup_commands = sut_config.clean_up_commands
sut_stop_commands = sut_config.kill_program_commands

id_rsa_location = slicify_config.id_rsa_location

def setup_sut_dependencies_single_node(node_ip):
    """
        @brief: Setup SUT dependencies on a single node using the script within sut_tools/
    """

    # Grab SSH key and node list from user_config
    id_rsa_location = slicify_config.id_rsa_location
    
    print("Setting up SUT dependencies on ", node_ip)
    destination =  node_ip + ':' + sut_config.sut_dir
    
    # Remove old SUT directory if it exists
    subprocess.run ([ 'ssh', node_ip, '-i', id_rsa_location,'-o','StrictHostKeyChecking=no','&&', 'rm -rf', sut_config.sut_dir ])
    
    # Copy SUT directory to node
    subprocess.run(['scp', '-r', '-i', id_rsa_location, '-o','StrictHostKeyChecking=no', sut_config.sut_dir, destination ])

    # Run script to setup dependencies from SUT tools
    subprocess.run ([ 'ssh', node_ip, '-i', id_rsa_location,'-o','StrictHostKeyChecking=no','&&', 'cd' , os.path.join(sut_config.sut_dir, sut_config.sut_tools_dir), '&&', './setup_sut_dependencies.sh' ])
    
    print("SUT dependencies succesfully set up on", node_ip)

def setup_sut_dependencies():
    """
        @brief: Setup SUT dependencies on all cluster nodes
    """

    for node_ip in slicify_config.cluster_nodes:
        setup_sut_dependencies_single_node(node_ip)


def install_sut():
    """
        @brief: Install SUT code on all cluster nodes
    """
    global sut_setup_commands, id_rsa_location

    # Run relevant SUT setup commands on all nodes
    for node_ip in slicify_config.cluster_nodes:
        for node, command in sut_setup_commands.items():
            if(node == node_ip):
                subprocess.run(['ssh', node_ip ,'-i', id_rsa_location,'-o','StrictHostKeyChecking=no','&&', command ])
    
def run_sut_test(test_key):
    """
        @brief: Run one test case (pointed to by test_key)
    """
    global sut_tests

    # Clear out old logs
    clean_up()

    # Run unit test
    subprocess.call(sut_tests[test_key], shell=True)

def verify_test_result(test_key):
    """
        @brief: Verify one test case result (pointed to by test_key)
    """
    
    global sut_verify

    # Verify unit test result
    subprocess.call(sut_verify[test_key], shell=True)

def collect_logs(test_key):
    """
        @brief: Collect logs for one test case (pointed to by test_key)
    """
    
    global sut_log_collect_commands

    # Collect logs for one unit test
    subprocess.call(sut_log_collect_commands[test_key], shell=True)

def clean_up():
    """
        @brief: Clean up after running tests
    """

    global sut_cleanup_commands
    # Clean up logs for one unit test
    for node_ip in slicify_config.cluster_nodes:
         subprocess.run(['ssh', node_ip ,'-i', id_rsa_location,'-o','StrictHostKeyChecking=no','&&', sut_cleanup_commands[node_ip] ], stdout = subprocess.DEVNULL, stderr = subprocess.DEVNULL)

def stop_sut():
    """
        @brief: Stop SUT
    """
    for node_ip in slicify_config.cluster_nodes:
        for node, command in sut_stop_commands.items():
            if(node == node_ip):
                subprocess.run(['ssh', node_ip ,'-i', id_rsa_location,'-o','StrictHostKeyChecking=no','&&', command ], stdout = subprocess.DEVNULL, stderr = subprocess.DEVNULL)
    
    time.sleep(5)

def copy_logs_to_dest(log_dest):
    """
        @brief: Copy logs over to destination directory
    """
    for node_ip in slicify_config.cluster_nodes:
        node_sut_logs_path = node_ip + ":" + os.path.join(sut_config.sut_logs_path, "*.log")
        print(node_sut_logs_path)
        subprocess.run(['scp','-r',node_sut_logs_path, log_dest])

def measure_test_runtime(test_key):
    """
        @brief: Get runtime of a unit test
        @return: Runtime of test
    """

    # Kill old SUT programs if any
    stop_sut()

    start = time.time()
    run_sut_test(test_key)
    end = time.time()

    stop_sut()
    
    elapsed_time = end - start
    return elapsed_time
