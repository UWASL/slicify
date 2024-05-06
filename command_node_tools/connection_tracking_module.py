#!/usr/bin/env python3
import os, re, socket, time
import subprocess
import shutil
import pandas as pd
import config_files.sut_config as sut_config
import config_files.slicify_config as slicify_config

import sut_control_module

id_rsa_location = slicify_config.id_rsa_location
full_results = [re.findall('^[\w\?\.]+|(?<=\s)\([\d\.]+\)|(?<=at\s)[\w\:]+', i) for i in os.popen('arp -a')]

stop_port = slicify_config.stop_port
stop_msg = b'STOP'

nodes_ip = slicify_config.cluster_nodes_ip
nodes = slicify_config.cluster_nodes

def pre_capture_phase():
    """
        @brief: Run pre-capture port detection on all nodes and generate a capture filter
    """

    # Create the log path on command_node if it does not exist because the capture script internally sends back each log to it after stopping
    if(os.path.isdir(slicify_config.comm_logs_path)):
        shutil.rmtree(slicify_config.comm_logs_path)

    os.makedirs(slicify_config.comm_logs_path) 

    # Replace config.py in slicify_tools on all cluster nodes
    with open(os.path.join(slicify_config.slicify_config_path, "capture_config.py"), "w") as tool_config_file:
        tool_config_file.write('filter_string = "' + slicify_config.filter_string + '"\n')    
        tool_config_file.write('stop_port = ' + str(slicify_config.stop_port) + '\n')
        tool_config_file.write('capture_filter_filename = "' + slicify_config.capture_filter_filename + '"\n')    
        tool_config_file.write('iface_name = "' + slicify_config.iface_name + '"\n')
        tool_config_file.write('id_rsa_location = "' + slicify_config.id_rsa_location + '"\n')
        tool_config_file.write('command_node_ip = "' + slicify_config.command_node_ip + '"\n')
        tool_config_file.write('comm_logs_path = "' + slicify_config.comm_logs_path + '"\n')
        tool_config_file.write('user_name = "' + slicify_config.user_name + '"\n')              
    
    
    for node_ip in slicify_config.cluster_nodes:
        destination =  node_ip + ':' + slicify_config.slicify_tools_path
        subprocess.run(['scp', '-r', '-i', id_rsa_location, '-o','StrictHostKeyChecking=no', os.path.join(slicify_config.slicify_config_path, "capture_config.py"), destination ])

    # Create list of hosts for parallel ssh
    with open(os.path.join(slicify_config.comm_logs_path, "hosts.txt"), 'w') as out_file:
        for ip in nodes_ip:
            out_file.write("%s\n" % ip)

    # Run pre_capture.py on all nodes    
    subprocess.run(['parallel-ssh', '-O', 'StrictHostKeyChecking=no', '-i', '-h', os.path.join(slicify_config.comm_logs_path, "hosts.txt"), '-t', '0','python3', os.path.join(slicify_config.slicify_tools_path, 'pre_capture.py'), '&'])
  
    print('Pre-capture procedures complete')

def capture_connections():
    """
        @brief: Capture communication for one unit test
    """
    print("Beginning distributed packet capture")
    
    open('flag.txt', 'w')  
    subprocess.Popen(['parallel-ssh', '-O', 'StrictHostKeyChecking=no', '-i', '-h', os.path.join(slicify_config.comm_logs_path, "hosts.txt"), '-t', '0', 'sudo', 'python3', os.path.join(slicify_config.slicify_tools_path, 'capture.py')])

def stop_capture():
    """
        @brief: Stop packet capture on all nodes by sending a STOP packet to stop_port
    """ 
    
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

    # Clean up hosts.txt
    if(os.path.isfile(os.path.join(slicify_config.comm_logs_path, "hosts.txt"))):
        os.remove(os.path.join(slicify_config.comm_logs_path, "hosts.txt"))
    

def merge_logs():
    """
        @brief: Merge all logs, sort them and identify transitive communication
    """
    # List all logs in comm_logs_path
    file_list = os.listdir(slicify_config.comm_logs_path)
    # print("Files: ", file_list)

    # os.chdir(slicify_config.comm_logs_path)
    # Open file3 in write mode to merge all packets
    with open(os.path.join(slicify_config.slicify_tools_path,'merged_packets.csv'), 'w') as outfile:
  
        # Iterate through list
        for name in file_list:    
            # Open each file in read mode
            with open(os.path.join(slicify_config.comm_logs_path, name), 'r') as infile:    
                # read the data from the files 
                # and write it in file3
                outfile.write(infile.read())
    
    subprocess.call("cp " + os.path.join(slicify_config.slicify_tools_path,'merged_packets.csv') + " " + slicify_config.comm_logs_path, shell=True)

    merged_packets_file_path = os.path.join(slicify_config.comm_logs_path, "merged_packets.csv")
    sorted_merged_file_path = os.path.join(slicify_config.comm_logs_path,'sorted_merged_packets.csv')

    # sorting packets depending on time_stamps
    dataFrame = pd.read_csv (merged_packets_file_path, header= None , dtype= str)
    dataFrame.sort_values( 0 , axis=0, ascending=True,inplace=True, na_position='first')
    dataFrame.to_csv (sorted_merged_file_path , index = False)

    # source _ destination _ lists
    df = pd.read_csv (sorted_merged_file_path, dtype = str )
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
    with open(os.path.join(slicify_config.comm_logs_path, 'final_unique_comms.txt'), 'w') as outfile:
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

def read_final_merged_log():
    """
        Read final merged logs to obtain unique pairs of communicating nodes
    """
    with open(os.path.join(slicify_config.comm_logs_path, 'final_unique_comms.txt'), 'r') as infile:
        file_lines = infile.readlines()
        comm_list = []

        for line in file_lines:
            ip_set = []
            ip_set.append((line.split()[0][2:-2]))
            ip_set.append((line.split()[2][1:-2]))
            comm_list.append(ip_set)
            uniq_comm_sets  = [set(comm_list[0])] 
            uniq_comm_lists = [comm_list[0]]
            for ip_set in comm_list:
                set_of_ip_set = set(ip_set) 
                if set_of_ip_set not in uniq_comm_sets:
                    uniq_comm_sets.append(set_of_ip_set)
                    uniq_comm_lists.append(ip_set)
    return uniq_comm_lists

def run_test_and_capture(test_key, elapsed_time):
    
    # Run pre-capture and create filters
    pre_capture_phase()

    # Kill old SUT programs if any
    sut_control_module.stop_sut()
    
    # Run test with capture
    capture_connections()
    sut_control_module.run_sut_test(test_key)
    time.sleep(elapsed_time)
    stop_capture()

    time.sleep(5)
    sut_control_module.stop_sut()   

    # Merge communication logs
    merge_logs()