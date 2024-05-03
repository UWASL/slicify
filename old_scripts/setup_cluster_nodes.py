#!/usr/bin/env python3
import os, re
import subprocess
import sys
import command_node_tools.config_files.slicify_config as slicify_config
import command_node_tools.config_files.sut_config as sut_config

# Grab SSH key and node list from user_config
id_rsa_location = sut_config.id_rsa_location
nodes = sut_config.nodes

# Copy cluster-node scripts to each node 
for node in nodes:
    print(node)
    destination =  node + ':~/'    # node1:~/
    subprocess.run(['scp','-i', id_rsa_location, '-o','StrictHostKeyChecking=no','node0:~/network_nodes/*', destination ])
    
# Install dependencies on each cluster node
for node in nodes:
    print(node)
    chrony_conf_destination = node + ':/etc/chrony'   
    subprocess.run ([ 'ssh' ,node, '-i', id_rsa_location,'-o','StrictHostKeyChecking=no','&&', 'cd' , '~/', '&&', 'bash', 'setup_nodes.sh' ])
    subprocess.run(['ssh', node,'-i', id_rsa_location,'-o','StrictHostKeyChecking=no','&&','sudo','scp','chrony.conf', chrony_conf_destination ])
    subprocess.run ([ 'ssh' ,node, '-i', id_rsa_location,'-o','StrictHostKeyChecking=no','&&', 'cd' , '~/', '&&', 'sudo', 'systemctl','restart', 'chronyd.service' ])


    
