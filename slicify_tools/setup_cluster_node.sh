#!/bin/bash

sudo apt update
sudo dpkg --configure -a
sudo apt install -y python3
sudo apt install -y python3-pip
sudo apt install -y python3
echo "wireshark-common wireshark-common/install-setuid boolean true" | sudo debconf-set-selections
sudo DEBIAN_FRONTEND=noninteractive apt-get -y install tshark
sudo python3 -m pip install pyshark
sudo python3 -m pip install pint
sudo python3 -m pip install psutil
pip3 install psutil 
sudo apt install -y python3-numpy
sudo apt install -y python3-pandas
sudo apt install -y screen
sudo apt install -y chrony
sudo systemctl start chronyd



