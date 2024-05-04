""" 
    Slicify internal configuration
"""

import os

# TODO
# Modify root dir path to match actual destination
slicify_root_dir = "/users/s2udayas/slicify/"
slicify_tools_dir = "slicify_tools"
slicify_config_dir = "command_node_tools/config_files"

slicify_tools_path = os.path.join(slicify_root_dir, slicify_tools_dir)
slicify_config_path = os.path.join(slicify_root_dir, slicify_config_dir)

comm_logs_path = os.path.join(slicify_root_dir, "comm_logs")

# Filter string used when capturing packets
filter_string = 'tcp || udp && tcp port not 443 && udp port not 123'

# Stop port?
stop_port = 13897

# Filename for capture filter
capture_filter_filename = os.path.join(slicify_tools_path, 'capture_filter')


"""
    Cluster configuration details

"""
# TODO
# Modify to match target cluster details!

iface_name = 'enp8s0d1'
id_rsa_location = '/users/s2udayas/.ssh/id_rsa'
user_name = "s2udayas"

command_node_ip = '10.10.1.1'
cluster_nodes = ['node1', 'node2', 'node3']
cluster_nodes_ip = ['10.10.1.2', '10.10.1.3', '10.10.1.4']
