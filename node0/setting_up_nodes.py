import os, re
import subprocess
import sys

# listting all the nodes 
full_results = [re.findall('^[\w\?\.]+|(?<=\s)\([\d\.]+\)|(?<=at\s)[\w\:]+', i) for i in os.popen('arp -a')]
nodes = []
for l in full_results:
    if ((l[0] != '?') and (l[0]!= 'control')):
        nodes.append(l[0])

for node in nodes:
    #print(node)
    destination =  node + ':/users/seba'    # node1:/users/seba
    #print(destination)
    chrony_conf_destination = node + ':/etc/chrony'
    subprocess.run(['scp','-i', '/users/seba/.ssh/id_rsa', '-o','StrictHostKeyChecking=no','node0:/users/seba/network_nodes/*', destination ])
    subprocess.run(['scp', '-i', '/users/seba/.ssh/id_rsa','node0:/users/seba/servers_clients/*', destination ])
    subprocess.run ([ 'ssh' ,node, '&&', 'cd' , '/users/seba/', '&&', 'bash', 'setup_nodes.sh' ])
    subprocess.run(['sudo','scp', 'node0:/users/seba/network_nodes/chrony.conf', chrony_conf_destination ])
    subprocess.run ([ 'ssh' ,node, '&&', 'cd' , '/users/seba/', '&&', 'sudo', 'systemctl','restart', 'chronyd.service' ])


    
