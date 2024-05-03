#!/usr/bin/env python3
import os, re, socket
import subprocess
import shutil
import pandas as pd
import command_node_tools.config_files.sut_config as sut_config
import command_node_tools.config_files.slicify_config as slicify_config

id_rsa_location = sut_config.id_rsa_location
full_results = [re.findall('^[\w\?\.]+|(?<=\s)\([\d\.]+\)|(?<=at\s)[\w\:]+', i) for i in os.popen('arp -a')]

stop_port = slicify_config.stop_port
stop_msg = b'STOP'

nodes_ip = slicify_config.cluster_nodes_ip
nodes = slicify_config.cluster_nodes

def pre_capture_phase():
    """
        @brief: Run pre-capture port detection on all nodes and generate a capture filter
    """

    # Create list of hosts for parallel ssh
    with open("hosts.txt", 'w') as out_file:
        for ip in nodes_ip:
            out_file.write("%s\n" % ip)

    # Run pre_capture.py on all nodes    
    subprocess.run(['parallel-ssh', '-i', '-h', 'hosts.txt', '-t', '0','python3.7', 'pre_capture.py'])

    # Clean up hosts.txt
    os.remove('hosts.txt')
    
    print('Pre-capture procedures complete')

def capture_connections():
    """
        @brief: Capture communication for one unit test
    """
    print("Beginning distributed packet capture")
    
    open('flag.txt', 'w')  
    subprocess.run(['parallel-ssh', '-i', '-h', 'hosts.txt', '-t', '0', 'sudo', 'python3.7', 'capture.py', '&'])

def stop_capture():
    """
        @brief: Stop packet capture on all nodes by sending a STOP packet to stop_port
    """
    
    # Create the log path on command_node if it does not exist because the capture script internally sends back each log to it after stopping
    if(os.path.isdir(slicify_config.comm_logs_path)):
        shutil.rmtree(slicify_config.comm_logs_path)

    os.makedirs(slicify_config.comm_logs_path) 

    # Stop packet capture on all nodes
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

def merge_logs():
    """
        @brief: Merge all logs, sort them and identify transitive communication
    """
    # List all logs in comm_logs_path
    file_list = os.listdir(slicify_config.comm_logs_path)

    os.chdir(slicify_config.comm_logs_path)
    # Open file3 in write mode to merge all packets
    with open('merged_packets.csv', 'w') as outfile:
  
        # Iterate through list
        for names in file_list:
    
            # Open each file in read mode
            with open(names) as infile:
    
                # read the data from the files 
                # and write it in file3
                outfile.write(infile.read())

    # sorting packets depending on time_stamps
    dataFrame = pd.read_csv ("merged_packets.csv", header= None , dtype= str)
    dataFrame.sort_values( 0 , axis=0, ascending=True,inplace=True, na_position='first')
    dataFrame.to_csv ('sorted_merged_packets.csv' , index = False)

    # source _ destination _ lists
    df = pd.read_csv ("sorted_merged_packets.csv", dtype = str )
    new_df = df.iloc [ : , 2:6 ]
    src_dest_lists = new_df.values.tolist()

    # unique communications
    uniq_comm_sets  = [ set(src_dest_lists[0])] #
    uniq_comm_lists = [src_dest_lists[0]]
    for l in src_dest_lists:
        set_of_l = set(l) #
        if set_of_l not in uniq_comm_sets:
            uniq_comm_sets.append(set_of_l)
            uniq_comm_lists.append(l)

    # time stamps of the unique communications
    time_stamps = { } 
    for comm in uniq_comm_lists: 
        new_key = uniq_comm_lists.index(comm)
        time_stamps[new_key] = []
        time_stamps[new_key].append([i for i, l in enumerate(src_dest_lists) if set(l) == set(comm) ])
    

    # final outtput [ src address ,  port number, dest address , port number, starting time, 
    # offset of starting time, ending time, offset of ending time ]
    with open('final.txt', 'w') as outfile:
        for key in time_stamps.keys():
            new_entry = uniq_comm_lists[key]
            time_index = time_stamps.get(key)
            starting_time_index = time_index[0][0]
            ending_time_index = time_index[0][-1]
            starting_time = df.iloc[starting_time_index,0]
            new_entry.append( df.iloc[starting_time_index,0])
            new_entry.append(df.iloc[starting_time_index,1])
            ending_time = df.iloc[ending_time_index,0]
            new_entry.append(df.iloc[ending_time_index,0])
            new_entry.append(df.iloc[ending_time_index,1])
            outfile.write("%s\n" % new_entry)
