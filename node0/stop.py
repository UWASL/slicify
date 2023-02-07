import socket
import pathlib
import os, re

# Make a directory named logs to collect all the logs inside it
p = pathlib.Path("logs/")
p.mkdir(parents=True, exist_ok=True) 


# Send a STOP packet to all other nodes 
# listing nodes using arp -a
full_results = [re.findall('^[\w\?\.]+|(?<=\s)\([\d\.]+\)|(?<=at\s)[\w\:]+', i) for i in os.popen('arp -a')]
hosts = []
port = 10000
for l in full_results:
    if ((l[0] != '?') and (l[0]!= 'control')):
        hosts.append(l[1][1:-1])
        

port = 10000
for host in hosts:
    # Create a TCP/IP socket
    sock = socket.socket( socket.AF_INET, socket.SOCK_STREAM)
    # Connect the socket to the port where the server is listening
    sock.connect(( host, port))
    # Send a STOP packet to all other nodes 
    sock.sendto( b"STOP", (host, port) )
    sock.close()