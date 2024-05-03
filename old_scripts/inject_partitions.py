#!/usr/bin/env python3
import os, re
import subprocess
import sys
import command_node_tools.config_files.sut_config as sut_config
import pathlib
import time
import signal
import glob
from subprocess import PIPE
from measure_app_time import elapsed_time

Application_logs_path = sut_config.Application_logs_path
App_path = sut_config.App_path
App_logs_path = App_path + '/logs'
tests_logs_path = App_path+'/tests_logs'
id_rsa_location = sut_config.id_rsa_location
App_destinantion = sut_config.App_destination
tests_logs_destination = App_destinantion + '/tests_logs'
ip_addresses_set = []
entries_list = []
comm_list = []
uniq_comm_lists = []
src_ip = ''
dst_ip = ''
waiting_time = int (5 * elapsed_time)
test_number = 0
final_logs_path = App_logs_path +'/final_logs.txt'

class TimeoutException(Exception):   # Custom exception class
    pass


def timeout_handler(signum, frame):   # Custom signal handler
    raise TimeoutException

signal.signal(signal.SIGALRM, timeout_handler)

# make tests logs directories
def make_test_logs_dir():
   global test_number 
   global tests_logs_path
   test_number = test_number + 1
   test_logs_path = tests_logs_path + '/test'+ str(test_number)
   p = pathlib.Path(test_logs_path)
   p.mkdir(parents=True, exist_ok=True)
   return(test_number)

def write_test_details():
   test_details_path = tests_logs_path + '/test'+ str(test_number) + '/test_details.txt'
   with open(test_details_path, 'w') as outfile:
      outfile.write("partion is injected between:   " + src_ip + '  and  ' + dst_ip + '\n')
      

# open final.txt
def read_final_logs():
  global entries_list
  with open(final_logs_path, "r") as infile: 
   entries_list = infile.readlines() 
  return(entries_list)


# get ips
def get_ip_pair():
  global uniq_comm_lists
  for line in entries_list:
    ip_set = []
    ip_set.append((line.split()[0][2:-2]))
    ip_set.append((line.split()[2][1:-2]))
    comm_list.append(ip_set)
  uniq_comm_sets  = [ set(comm_list[0])] 
  uniq_comm_lists = [comm_list[0]]
  for ip_set in comm_list:
    set_of_ip_set = set(ip_set) 
    if set_of_ip_set not in uniq_comm_sets:
        uniq_comm_sets.append(set_of_ip_set)
        uniq_comm_lists.append(ip_set)
  return(uniq_comm_lists)


# split ips
def split_ips():
    global src_ip
    global dst_ip 
    src_ip = ip_set[0]
    print('first ip = ', src_ip)
    dst_ip = ip_set[1]
    print('second ip = ', dst_ip)
    
 # drop connection   
def drop_Connection():
    #run iptable command for DROP with ip src being the other ip 
    #sudo iptables -A INPUT -s ip -j DROP
    subprocess.run(['ssh', src_ip, '&&', 'sudo', 'iptables', '-A', 'INPUT', '-s', dst_ip, '-j', 'DROP'])

# clean up
def clean_up():
   #clean up old logs
   subprocess.run(['python3', 'clean_up.py', '&'])

# wait for 30 sec
def wait():
   time.sleep(30)


# run application
def run_program():  
    subprocess.run (['python3', 'run_program.py', '&'])

# heal the partion 
def heal_partion():
    # heal partion from the same node with the same ip address.
    # sudo iptables -D INPUT -s ip -j DROP
    subprocess.run(['ssh', src_ip, '&&', 'sudo', 'iptables', '-D', 'INPUT', '-s', dst_ip, '-j', 'DROP'])

# add tests logs
def add_reported_logs():
   test_logs_destination = tests_logs_destination + '/test' + str(test_number)
   for key in Application_logs_path.keys():
    # get Application reported logs path
    reported_logs_path = Application_logs_path[key]
    # get the latest log
    latest_test_log = subprocess.run(['ssh', key, '&&', 'ls', reported_logs_path , '-t', '|', 'head', '-1'], stdout= PIPE, stderr= PIPE)
    latest_test_log = latest_test_log.stdout.decode("utf-8").rstrip("\n")
    latest_test_log = reported_logs_path + latest_test_log 
    subprocess.run(['ssh', key,'&&' ,'scp','-i', id_rsa_location,'-o','StrictHostKeyChecking=no',latest_test_log, test_logs_destination, '&'])


def passed_test():
    test_details_path = tests_logs_path + '/test'+ str(test_number) + '/test_details.txt'
    with open(test_details_path, 'a') as outfile:
      outfile.write("Test Passed"  + '\n')
      outfile.close()

def failed_test():
    test_details_path = tests_logs_path + '/test'+ str(test_number) + '/test_details.txt'
    with open(test_details_path, 'a') as outfile:
      outfile.write("Failed test " + '\n')
      outfile.write("Waited for  " + str (waiting_time) + " s" + "  without response" + '\n' )
      outfile.close()

if __name__ == '__main__':
    
    read_final_logs()
    #print (entries_list)
    get_ip_pair()
    #print(uniq_comm_lists)
    
    for ip_set in uniq_comm_lists:
       make_test_logs_dir()
       print(ip_set)
       split_ips()
       write_test_details()
       drop_Connection()
       wait()
       signal.alarm(waiting_time)
       try:
        run_program()
       except TimeoutException:
          heal_partion()
          wait()
          failed_test()
          add_reported_logs()
          continue
       else:
          signal.alarm(0)
          heal_partion()
          wait()
          passed_test()
          add_reported_logs()
    clean_up()
    
    
