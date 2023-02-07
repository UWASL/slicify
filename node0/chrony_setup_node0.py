import subprocess


# run this script using sudo python3 chrony_setup_node0.py
with open('server_chrony.txt' , 'r') as file:
    new_confg = file.read()

f = open(r"/etc/chrony/chrony.conf", "r+")
f.truncate(0)
f.write(new_confg)
f.close()

# add commands to restart chrony after making these changes to the config file
subprocess.run (['sudo', 'systemctl', 'restart', 'chronyd.service'])

#sudo firewall-cmd --add-service=ntp --permanent

#sudo firewall-cmd --reload
