#!/usr/bin/env python3

#!/usr/bin/env python3
import os, time
import subprocess
import config_files.slicify_config as slicify_config
import config_files.sut_config as sut_config

import slicify_deployment
import sut_control_module
import connection_tracking_module

def controller_main():

    # Deploy slicify across all cluster nodes
    # slicify_deployment.deploy_slicify_on_all_nodes()

    # Deploy and install SUT
    # sut_control_module.setup_sut_dependencies()
    # sut_control_module.install_sut()

    # Run test cases

    for test_key, run_cmd in sut_config.run_program_commands.items():

    #     # Run test and capture communications
        connection_tracking_module.run_test_and_capture(test_key)
    
    # sut_control_module.run_sut_test("3WayComms")
    # time.sleep(5)
    # connection_tracking_module.stop_capture()

if(__name__ == "__main__"):
    controller_main()