#!/usr/bin/env python3
# capture.py

import pyshark
import subprocess
import socket
import pint
import config
import os
import command_node_tools.config_files.sut_config as sut_config
import command_node_tools.config_files.slicify_config as slicify_config



iface_name = slicify_config.iface_name     #'enp6s0f0'
filter_string = config.filter_string  #'tcp || udp && ip && tcp port not 443 && udp port not 123'
hostname = socket.gethostname().split(".")[0]
filename = f'{hostname}_captured_packets.csv' 

destination = os.path.join(slicify_config.comm_logs_path) #'node0:/users/seba/logs'  

id_rsa_location = slicify_config.id_rsa_location 
capture_filter_filename = config.capture_filter_filename
time_offset = ''
tcp_ports = set()
udp_ports = set()
packets = set()
logs_destination = destination
master_node_ip = slicify_config.command_node_ip


def  get_offset(): 
 global time_offset
 process = subprocess.run (['chronyc', '-n', 'sourcestats'], capture_output=True)
 time_offset = process.stdout.decode().splitlines()[3]. split()[-2]
 reg = pint.UnitRegistry()
 offset = reg(time_offset).to("s").magnitude
 return time_offset


def read_capture_filter():
   global filter_string
   with open (capture_filter_filename) as infile:
      filter_string = infile.read()

def capture():
  capture = pyshark.LiveCapture(
    interface=iface_name
    ,bpf_filter=filter_string)
 
  
  for packet in capture.sniff_continuously():
      
      
      if  hasattr(packet, 'tcp'):
#             ts = packet.sniff_timestamp
#             ts = f"{ts.split('.')[0][-3:]}.{ts.split('.')[-1]}" # avoid rounding floats and losing percision
#             ts = float(ts) + offset
#             ts = str(ts)
         if (packet.tcp.flags.int_value == 2 or packet.tcp.flags.int_value == 11 ):    
            packets.add(  packet.sniff_timestamp + ',' + time_offset + ',' + packet.ip.src + ',' + str(packet.tcp.srcport)+ ',' +packet.ip.dst + ',' + str (packet.tcp.dstport)) #+ ',' + packet.tcp.flags.showname)
            #print('just arrived TCP packet ', packet.sniff_timestamp , 'source ip:' ,packet.ip.src , 'tcp source port:' ,packet.tcp.srcport,' dest ip:' ,packet.ip.dst , ' tcp dest port:' ,packet.tcp.dstport)
      
                 
      if hasattr(packet, 'udp'):
#             ts = packet.sniff_timestamp
#             ts = f"{ts.split('.')[0][-3:]}.{ts.split('.')[-1]}" # avoid rounding floats and losing percision
#             ts = float(ts) + offset
#             ts = str(ts)
           
           packets.add( packet.sniff_timestamp + ',' + time_offset + ',' +packet.ip.src + ',' + str(packet.udp.srcport) + ',' + packet.ip.dst  + ',' + str(packet.udp.dstport))
           #print('just arrived UDP packet ', packet.sniff_timestamp ,'source ip:' ,packet.ip.src , 'udp source port:' ,packet.udp.srcport,' dest ip:' ,packet.ip.dst , ' udp dest port:' ,packet.udp.dstport)
      
      if ( packet.ip.src == master_node_ip):
                  break 
      
  return packets

def write_captured_packets():
 master_ip = ',' + master_node_ip + ','
 with open(filename, 'w') as out_file:
  for packet in packets:
        if (master_ip not in packet):
          out_file.write("%s\n" % packet)
        
       

def send_captured_packets(): #send captured packets to node0
   subprocess.run(['scp', '-i', id_rsa_location, '-o','StrictHostKeyChecking=no', filename, logs_destination ])	


# call functions

if __name__ == '__main__':
    get_offset()
    read_capture_filter()
    capture()
    print("Done capture")
    write_captured_packets()
    print('Done writing')
    send_captured_packets()
    print('Done')