import os
import pathlib
import pandas as pd 
import time
import csv
import user_config

logs_path = user_config.App_path + '/logs'
file_list = os.listdir(logs_path)

   
os.chdir(logs_path)
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
with open('final_logs.txt', 'w') as outfile:
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
