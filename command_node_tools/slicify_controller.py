#!/usr/bin/env python3

#!/usr/bin/env python3
import os
import subprocess
import config_files.slicify_config as slicify_config
import config_files.sut_config as sut_config

import slicify_deployment
import sut_control_module

def controller_main():

    # Deploy slicify across all cluster nodes
    # slicify_deployment.deploy_slicify_on_all_nodes()

    # Deploy and install SUT
    sut_control_module.setup_sut_dependencies()
    sut_control_module.install_sut()


if(__name__ == "__main__"):
    controller_main()