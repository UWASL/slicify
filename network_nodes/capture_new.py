#!/usr/bin/env python3
# capture.py

import pyshark
import psutil
import re
import subprocess
import socket
import pint
import time 
import config

iface_name = config.iface_name     #'enp6s0f0'
filter_string = config.filter_string  #'tcp || udp && ip && tcp port not 443 && udp port not 123'
hostname = socket.gethostname().split(".")[0]
filename = f'{hostname}_captured_packets.csv' 
destination = config.destination #'node0:/users/seba/logs'    # node1:~/
id_rsa_location = config.id_rsa_location 
time_offset = ''
tcp_ports = set()
udp_ports = set()
packets = set()


def  get_offset(): 
 global time_offset
 process = subprocess.run (['chronyc', '-n', 'sourcestats'], capture_output=True)
 time_offset = process.stdout.decode().splitlines()[3]. split()[-2]
 reg = pint.UnitRegistry()
 offset = reg(time_offset).to("s").magnitude
 return time_offset


def get_tcp_open_ports():
 process = subprocess.run(['netstat', '-ant'], capture_output=True)
 report = process.stdout.decode().splitlines()
 for i in report[2:]:
       tcp_ports.add(i.split()[3].split(":")[-1])
 return tcp_ports


def get_udp_open_ports():
 process = subprocess.run(['netstat', '-anu'], capture_output=True)
 report = process.stdout.decode().splitlines()
 for i in report[2:]:
        udp_ports.add(i.split()[3].split(":")[-1])       
 return udp_ports


def generate_capturing_filter():
  global filter_string      
  for port in udp_ports:
        if(port == "*"):
              continue 
        filter_string += ' && udp port not ' + str(port) + ' '

  for port in tcp_ports:
         if(port == "*"):
                 continue 
         filter_string += '&& tcp port not ' + str(port) + ' '
  return filter_string




def capture():
  capture = pyshark.LiveCapture(
    interface=iface_name,
    bpf_filter=filter_string)
 

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
  return packets

def write_captured_packets():
 with open(filename, 'w') as out_file:
  for packet in packets:
        if ('10.10.1.1' not in packet):
            out_file.write("%s\n" % packet)
        
       

def send_captured_packets(): #send captured packets to node0
   subprocess.run(['scp', '-i', id_rsa_location, '-o','StrictHostKeyChecking=no', filename, destination ])	


# call functions

if __name__ == '__main__':
    get_offset()
    get_tcp_open_ports()
    #for port in tcp_ports:
        #print('tcp port' , port , '  ')
    get_udp_open_ports()
    #for port in udp_ports:
        #print ( 'udp port' ,port , '  ')
    generate_capturing_filter()
    #print( filter_string )
    capture()
    write_captured_packets()
    send_captured_packets()