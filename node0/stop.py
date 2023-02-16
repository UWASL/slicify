import socket
import pathlib
import os, re
import config


# Make a directory named logs to collect all the logs inside it
p = pathlib.Path("logs/")
p.mkdir(parents=True, exist_ok=True) 


# Send a STOP packet to all other nodes 
# listing nodes using arp -a
full_results = [re.findall('^[\w\?\.]+|(?<=\s)\([\d\.]+\)|(?<=at\s)[\w\:]+', i) for i in os.popen('arp -a')]
hosts = []
stop_port = config.stop_port
for l in full_results:
    if ((l[0] != '?') and (l[0]!= 'control')):
        hosts.append(l[1][1:-1])
        

for host in hosts:
    try:
        # Create a TCP/IP socket
        sock = socket.socket( socket.AF_INET, socket.SOCK_STREAM)
        # Connect the socket to the port where the server is listening
        sock.connect(( host,stop_port))
        # Send a STOP packet to all other nodes 
        sock.sendto( b"STOP", (host, stop_port) )
        sock.close()
    except Exception as e:
        print(e)
        # sock.close()