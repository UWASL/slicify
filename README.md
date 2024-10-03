# Slicify
This repository contains the code from our paper titled _Slicify: Fault Injection Testing for Network Partitions_ at MASCOTS 2024. Please cite our paper if you are using the code from this repository.

```
  Khaleel, S., Udayashankar, S., and Al-Kiswany, S., 2024, October. Slicify: Fault Injection Testing for Network Partitions. In 2024 32nd International Symposium on the Modeling, Analysis, and Simulation of Computer and Telecommunication Systems. IEEE
```

# Preparation

1. Install dependencies. This code was tested with Ubuntu 22.04.
   ```
     sudo apt update
     sudo apt install python3
   ```
   The remaining dependencies for cluster and command nodes are installed by the scripts _slicify_tools/setup_command_node.sh_ and _slicify_tools/setup_cluster_node.sh_ automatically when Slicify is deployed for the first time.

2. Edit configuration files. The following configuration files need to be modified in _command_node_tools/config_files_:
   -  _slicify_config.py_: Modify the first section with the correct Slicify configurations (such as root directory path). Modify the second section with target cluster information (interfaces and command/cluster node IPs). Make sure to edit SSH-related information as well.
   -  _sut_config.py_: This file contains SUT-related information such as deployment commands, unit test execution commands, etc. Usually, these point to SUT scripts which are called for each function.
   - _capture_config.py_: Interface name for packet capture on each cluster node. Edit SSH information here too (used by cluster nodes to log into the command node).
   - _chrony.conf_: Used by chrony to sync clocks using NTP. Modify if necessary.

## SUT (Application) preparation
The SUT needs to implement the functions called by _sut_control_module.py_ (such as deployment and build). Usually, this would mean implementing shell scripts and adding pointers to their paths into _sut_config.py_. An example client-server program and its necessary SUT scripts have been provided along with this repository. The _sample_client_server_ directory contains a simple client-server program implemented in Python. The _sample_client_server/sut_tools/_ directory contains the following scripts:

  - _1WayComms.sh_ and _3WayComms.sh_: Runs unit tests for one and 3 client-server pairs. 
  - _run_client.sh_ and _run_server.sh_: Runs the client and server respectively using the provided command line arguments.
  - _install_sut.sh_ and _setup_sut_dependencies.sh_: Setup and install SUT.

# Running the code
1. The following command reads the relevant configuration files, deploys Slicify and the SUT, and runs each unit test as follows:
   ```
     python3 command_node_tools/slicify_controller.py
   ```

   For each unit test, it measures fault-free time and tracks communications to prepare the global connection list. After this, it inserts partitions between each node pair and reruns the test. Finally, it isolates each node and runs the test. All results are recorded and reported. Further details can be found in our paper.
