#!/usr/bin/env python3
# capture.py

import pyshark
import psutil
import re
import subprocess
import socket
import pint
import time 

process = subprocess.run (['chronyc', '-n', 'sourcestats'], capture_output=True)
time_offset = process.stdout.decode().splitlines()[3]. split()[-2]
reg = pint.UnitRegistry()
offset = reg(time_offset).to("s").magnitude



process = subprocess.run(['netstat', '-ant'], capture_output=True)
report = process.stdout.decode().splitlines()
#with open('blah.txt', 'w') as out_file:
   #for item in report:
#         # write each item on a new line
        #out_file.write("%s\n" % item)
#print('Done')      

tcp_ports = set()
for i in report[2:]:
       #print("Line:", i, i.split()[3].split(".")[-1])
       tcp_ports.add(i.split()[3].split(":")[-1])
#for port in tcp_ports:
   #print ( 'tcp port' , port , '  ')
# with open('blah2.txt', 'w') as out_file:
#    for i in tcp_ports:
#         out_file.write("%s\n" % i)
#    print('Done')     


process = subprocess.run(['netstat', '-anu'], capture_output=True)
report = process.stdout.decode().splitlines()
udp_ports = set()
for i in report[2:]:
         udp_ports.add(i.split()[3].split(":")[-1])
        
#     #return ports
#for port in udp_ports:
   #print ( 'udp port' ,port , '  ')



# #iface_name = input("Enter interface name")
iface_name = 'enp6s0f0'

filter_string = 'tcp || udp && ip && tcp port not 443 && udp port not 123'

for port in udp_ports:
        if(port == "*"):
              continue 
        filter_string += ' && udp port not ' + str(port) + ' '

for port in tcp_ports:
         if(port == "*"):
                 continue 
         filter_string += '&& tcp port not ' + str(port) + ' '

# print( filter_string )
capture = pyshark.LiveCapture(
    interface=iface_name,
    bpf_filter=filter_string
 )


packets = set()
for packet in capture.sniff_continuously():

        if hasattr(packet, 'tcp'):
#             ts = packet.sniff_timestamp
#             ts = f"{ts.split('.')[0][-3:]}.{ts.split('.')[-1]}" # avoid rounding floats and losing percision
#             ts = float(ts) + offset
#             ts = str(ts)
            packets.add(  packet.sniff_timestamp + ',' + time_offset + ',' + packet.ip.src + ',' + str(packet.tcp.srcport)+ ',' +packet.ip.dst + ',' + str (packet.tcp.dstport))
            #print('just arrived TCP packet ', packet.sniff_timestamp , 'source ip:' ,packet.ip.src , 'tcp source port:' ,packet.tcp.srcport,' dest ip:' ,packet.ip.dst , ' tcp dest port:' ,packet.tcp.dstport)
        if hasattr(packet, 'udp'):
#             ts = packet.sniff_timestamp
#             ts = f"{ts.split('.')[0][-3:]}.{ts.split('.')[-1]}" # avoid rounding floats and losing percision
#             ts = float(ts) + offset
#             ts = str(ts)
           packets.add( packet.sniff_timestamp + ',' + time_offset + ',' +packet.ip.src + ',' + str(packet.udp.srcport) + ',' + packet.ip.dst  + ',' + str(packet.udp.dstport))
           #print('just arrived UDP packet ', packet.sniff_timestamp ,'source ip:' ,packet.ip.src , 'udp source port:' ,packet.udp.srcport,' dest ip:' ,packet.ip.dst , ' udp dest port:' ,packet.udp.dstport)
        if (packet.ip.src == "10.10.1.1" ):
            break 

hostname = socket.gethostname().split(".")[0]
filename = f'{hostname}_captured_packets.csv' 
with open(filename, 'w') as out_file:
  for packet in packets:
        if ('10.10.1.1' not in packet):
            out_file.write("%s\n" % packet)
        
       


destination = 'node0:/users/seba/logs'    # node1:~/
subprocess.run(['scp', filename, destination ])	

