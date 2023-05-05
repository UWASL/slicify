# RUN THIS IN NODE0 DIRECTORY USING python3 test_run.py
import user_config
import subprocess
import time
import os
from threading import Thread

flag = False
nodes = user_config.nodes
nodes_ip = user_config.nodes_ip
id_rsa_location = user_config.id_rsa_location
App_path = user_config.App_path
with open("hosts.txt", 'w') as out_file:
  for ip in nodes_ip:
    out_file.write("%s\n" % ip)

def clean_up():
    logs_path = App_path + '/logs'
    # remove the old content in logs in node0
    subprocess.run(['rm','-r' , logs_path])
    print('old logs deleted')
    #remove the old tests logs in node0 if exists
    tests_logs_path = App_path + '/tests_logs'
    subprocess.run(['rm','-r' ,tests_logs_path])
    print('old tests logs deleted')
    #remove wireshark tmp files
    subprocess.run(['parallel-ssh', '-i', '-h', 'hosts.txt', '-t', '0', 'cd', '/tmp/', '&&', 'sudo' ,'rm','-f', 'wiresha*'])

def send_user_config():
    for node in nodes:
        source = App_path+'/user_config.py'
        destination =  node + ':~/'
        subprocess.run(['scp', '-i', id_rsa_location,'-o','StrictHostKeyChecking=no',source, destination ])

def start_capturing():
    global flag 
    flag = True
    subprocess.run(['python3', 'start_capturing.py'])
    


def inject_partions():
    subprocess.run(['rm', '-r', 'flag.txt'])
    subprocess.run(['python3', 'set_up_program.py', '&'])
    time.sleep(10)
    subprocess.run(['python3', 'run_program.py','&'])
    time.sleep(5)
    subprocess.run(['python3', 'stop.py',])
    time.sleep(30)
    subprocess.run(['python3', 'edit_logs.py'])
    time.sleep(5)
    



if __name__ == '__main__':
    clean_up()
    send_user_config()
    time.sleep(10)
    #inject_partions() 
# create a thread
    thread_1 = Thread(target=start_capturing)
    thread_2 = Thread(target=inject_partions)
    thread_1.start()
    while not os.path.exists('flag.txt'):
        time.sleep(1)
    thread_2.start()
    thread_1.join()
    thread_2.join()
 
