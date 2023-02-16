import os, re
import subprocess


# listting all the nodes ip addresses 
full_results = [re.findall('^[\w\?\.]+|(?<=\s)\([\d\.]+\)|(?<=at\s)[\w\:]+', i) for i in os.popen('arp -a')]
nodes_ip = []
nodes = []
for l in full_results:
    if ((l[0] != '?') and (l[0]!= 'control')):
        nodes_ip.append(l[1][1:-1])
        nodes.append(l[0])

#writing hosts.txt
with open("hosts.txt", 'w') as out_file:
  for ip in nodes_ip:
    out_file.write("%s\n" % ip)


for node in nodes:
    print(node)
    destination =  node + ':/users/seba'    # node1:/users/seba
    #subprocess.run( ['ssh', node, 'cd','/var/tmp', 'rm', '-r', '*'] )
    subprocess.run(['scp','node0:/users/seba/network_nodes/capture_new.py', destination ])
    subprocess.run(['scp','node0:/users/seba/node0/config.py', destination ])
    subprocess.call("ssh seba@" + node + " rm *_captured_packets.csv", shell=True)
    
    
subprocess.run(['parallel-ssh', '-i', '-h', 'hosts.txt', '-t', '0', 'sudo', 'python3.7', 'capture_new.py', '&'])


