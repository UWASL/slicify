import subprocess


# chrony configuration for clients.
# run this script using sudo python3 chrony_setup_clients.py
with open('clients_chrony.txt' , 'r') as file:
    new_confg = file.read()


f = open(r"/etc/chrony/chrony.conf", "r+")
f.truncate(0)
f.write(new_confg)
f.close()

# add commands to restart chrony after making changes to the config file

subprocess.run (['sudo', 'systemctl', 'restart', 'chronyd.service'])
