#!/usr/bin/env python3
import os
import subprocess
import config_files.slicify_config as slicify_config
import config_files.sut_config as sut_config

def deploy_slicify_on_all_nodes():
    # Grab SSH key and node list from user_config
    id_rsa_location = slicify_config.id_rsa_location
    nodes = slicify_config.cluster_nodes

    # Copy slicify internal tools to each node 
    for node in nodes:
        print("Copying slicify to", node)
        
        subprocess.run ([ 'ssh', node, '-i', id_rsa_location,'-o','StrictHostKeyChecking=no','&&', 'mkdir' , slicify_config.slicify_root_dir ])
        destination =  node + ":" + slicify_config.slicify_root_dir + "/../"    # node1:~/
        subprocess.run(['scp', '-r', '-i', id_rsa_location, '-o','StrictHostKeyChecking=no',slicify_config.slicify_root_dir, destination ])

    # Setup command node - This script is assumed to be running on the command node
    subprocess.call("cd " + os.path.join(slicify_config.slicify_root_dir, slicify_config.slicify_tools_dir) + "&& ./setup_command_node.sh", shell=True)
        
    # Install slicify dependencies on each cluster node
    for node in nodes:
        print("Setting up slicify on", node)
        chrony_conf_destination = node + ':/etc/chrony'
        
        subprocess.run ([ 'ssh', node, '-i', id_rsa_location,'-o','StrictHostKeyChecking=no','&&', 'cd' , os.path.join(slicify_config.slicify_root_dir, slicify_config.slicify_tools_dir), '&&', './setup_cluster_node.sh' ])
        subprocess.run(['ssh', node,'-i', id_rsa_location,'-o','StrictHostKeyChecking=no','&&','sudo','scp','chrony.conf', chrony_conf_destination ])
        subprocess.run (['ssh', node, '-i', id_rsa_location,'-o','StrictHostKeyChecking=no','&&', 'sudo', 'systemctl','restart', 'chronyd.service' ])
    
    
if(__name__ == "__main__"):
    deploy_slicify_on_all_nodes()