import os, re
import subprocess
import sys
import config
import user_config

id_rsa_location = user_config.id_rsa_location
nodes = user_config.nodes
#setting up the nodes
for node in nodes:
    print(node)
    destination =  node + ':~/'    # node1:~/
    subprocess.run(['scp','-i', id_rsa_location, '-o','StrictHostKeyChecking=no','node0:~/network_nodes/*', destination ])
    

for node in nodes:
    print(node)
    chrony_conf_destination = node + ':/etc/chrony'   
    subprocess.run ([ 'ssh' ,node, '-i', id_rsa_location,'-o','StrictHostKeyChecking=no','&&', 'cd' , '~/', '&&', 'bash', 'setup_nodes.sh' ])
    subprocess.run(['ssh', node,'-i', id_rsa_location,'-o','StrictHostKeyChecking=no','&&','sudo','scp','chrony.conf', chrony_conf_destination ])
    subprocess.run ([ 'ssh' ,node, '-i', id_rsa_location,'-o','StrictHostKeyChecking=no','&&', 'cd' , '~/', '&&', 'sudo', 'systemctl','restart', 'chronyd.service' ])


    
