#!/usr/bin/env python3

#!/usr/bin/env python3
import os, time
import shutil, signal
import config_files.slicify_config as slicify_config
import config_files.sut_config as sut_config
import math

import slicify_deployment
import sut_control_module
import connection_tracking_module
import partition_injection_module
import signal_module

def controller_main():

    # Deploy slicify across all cluster nodes
    # slicify_deployment.deploy_slicify_on_all_nodes()

    # # Deploy and install SUT
    # sut_control_module.setup_sut_dependencies()
    # sut_control_module.install_sut()

    # Run test cases

    # Make test log dir 
    if(os.path.isdir(sut_config.sut_test_logs_path)):
        shutil.rmtree(sut_config.sut_test_logs_path)
    
    os.makedirs(sut_config.sut_test_logs_path)

    for test_key in sut_config.run_program_commands.keys():

        if(test_key != "1WayComms"):
            continue

        print("Analyzing test:", test_key)


        print("Running fault free execution")
        # Measure fault-free execution time
        test_run_time = sut_control_module.measure_test_runtime(test_key)
        time.sleep(5)
        
        # Run test and capture communications
        print("Capturing communication")
        connection_tracking_module.run_test_and_capture(test_key, test_run_time)
        time.sleep(5)
        communicating_node_pairs = connection_tracking_module.read_final_merged_log()

        print("Total communicating node pairs:", len(communicating_node_pairs))

        # Make test log root directory
        test_log_rootdir_path = os.path.join(sut_config.sut_test_logs_path, test_key)
        os.mkdir(test_log_rootdir_path)

        # Set timeout handling function
        signal_module.set_timeout_handler()

        # Test for partial partition impact
        for node_pair in communicating_node_pairs:

            print("Inserting partition between nodes", node_pair)
            partition_injection_module.inject_partial_partition(node_pair[0], node_pair[1])
            time.sleep(5)
   
            try:
                # Set SIGALRM in case test hits an infinite loop or stonewalls
                signal.alarm(3 * math.ceil(test_run_time))

                sut_control_module.run_sut_test(test_key)
            
                # # Wait 3x the fault free execution time before collecting results
                # time.sleep(3 * test_run_time)
            except signal_module.TimeoutException:
                print("\t Woke up due to SIGALRM. Stopping test and collecting logs")
                sut_control_module.stop_sut()
            else:
                print("\t Test completed. Collecting result now")
                sut_control_module.stop_sut()
            
            partition_injection_module.heal_partial_partition(node_pair[0], node_pair[1])

            print("Copying SUT logs from all nodes")
            
            test_log_dest = os.path.join(test_log_rootdir_path, "test_" + str(test_key) + "_partial_" + str(node_pair[0]) + "_" + str(node_pair[1]))
            os.mkdir(test_log_dest)
            sut_control_module.copy_logs_to_dest(test_log_dest)
    
        # test_log_rootdir_path = os.path.join(sut_config.sut_test_logs_path, test_key)
        # test_log_dest = os.path.join(test_log_rootdir_path, "test_" + str(test_key) + "_partial_" + str("test1"))
        # os.mkdir(test_log_dest)
        # sut_control_module.copy_logs_to_dest(test_log_dest)       


if(__name__ == "__main__"):
    controller_main()