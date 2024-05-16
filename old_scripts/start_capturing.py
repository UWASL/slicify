#!/usr/bin/env python3
import os, re
import subprocess
import command_node_tools.config_files.sut_config as sut_config

id_rsa_location = sut_config.id_rsa_location
full_results = [re.findall('^[\w\?\.]+|(?<=\s)\([\d\.]+\)|(?<=at\s)[\w\:]+', i) for i in os.popen('arp -a')]
nodes_ip = sut_config.nodes_ip
nodes = sut_config.nodes



# writing hosts.txt
with open("hosts.txt", 'w') as out_file:
  for ip in nodes_ip:
    out_file.write("%s\n" % ip)



# run pre_capture.py on all nodes    
subprocess.run(['parallel-ssh', '-i', '-h', 'hosts.txt', '-t', '0','python3.7', 'pre_capture.py'])
print('Done pre capturing')



#run capture_new.py on all nodes 
print('capture started') 
open('flag.txt', 'w')  
subprocess.run(['parallel-ssh', '-i', '-h', 'hosts.txt', '-t', '0', 'sudo', 'python3.7', 'capture.py', '&'])


