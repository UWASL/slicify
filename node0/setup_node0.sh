#!/bin/bash

sudo apt update
sudo apt install python3.7
sudo apt install python3-pip
sudo apt install python3.7-dev
sudo dpkg --configure -a
echo "wireshark-common wireshark-common/install-setuid boolean true" | sudo debconf-set-selections
sudo DEBIAN_FRONTEND=noninteractive apt-get -y install tshark
sudo python3.7 -m pip install pyshark 
sudo python3.7 -m pip install pint
sudo python3.7 -m pip install psutil
sudo pip3 install psutil 
sudo apt-get install pssh
sudo apt install python3-numpy
sudo apt install python3-pandas
sudo apt install chrony -y
sudo systemctl start chronyd
sudo apt install firewalld
sudo systemctl enable firewalld
sudo systemctl start firewalld
sudo firewall-cmd --add-service=ntp --permanent
sudo firewall-cmd --reload
