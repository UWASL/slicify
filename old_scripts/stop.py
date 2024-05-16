#!/usr/bin/env python3
import socket
import pathlib
import os, re
import command_node_tools.config_files.slicify_config as slicify_config
import command_node_tools.config_files.sut_config as sut_config

# Make a directory named logs to collect all the logs inside it
logs_path= sut_config.App_path + "/logs"
os.mkdir(logs_path) 


# Send a STOP packet to all other nodes 
# listing nodes using arp -a
#full_results = [re.findall('^[\w\?\.]+|(?<=\s)\([\d\.]+\)|(?<=at\s)[\w\:]+', i) for i in os.popen('arp -a')]

nodes_ip = sut_config.nodes_ip
stop_port = slicify_config.stop_port
stop_msg = b'STOP'

        

for ip in nodes_ip:
    try:
        # Create a TCP/IP socket
        sock = socket.socket( socket.AF_INET, socket.SOCK_STREAM)
        # Connect the socket to the port where the server is listening
        sock.connect(( ip,stop_port))
        # Send a STOP packet to all other nodes 
        sock.sendto( stop_msg, (ip, stop_port) )
        sock.close()
    except Exception as e:
        print(e)
        # sock.close()
