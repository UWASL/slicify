#!/bin/bash

sudo apt update
sudo dpkg --configure -a
sudo apt install python3.7
sudo apt install python3-pip
sudo apt install python3.7-dev
echo "wireshark-common wireshark-common/install-setuid boolean true" | sudo debconf-set-selections
sudo DEBIAN_FRONTEND=noninteractive apt-get -y install tshark
sudo python3.7 -m pip install pyshark
sudo python3.7 -m pip install pint
sudo python3.7 -m pip install psutil
sudo pip3 install psutil 
sudo apt install python3-numpy
sudo apt install python3-pandas
sudo apt install screen
sudo apt install chrony -y
sudo systemctl start chronyd



