#!/bin/bash

sudo apt update
sudo apt install -y python3
sudo apt install -y python3-pip
sudo apt install -y python3-dev
sudo dpkg --configure -a
echo "wireshark-common wireshark-common/install-setuid boolean true" | sudo debconf-set-selections
sudo DEBIAN_FRONTEND=noninteractive apt-get -y install tshark
python3 -m pip install pyshark 
python3 -m pip install pint
python3 -m pip install psutil
pip3 install psutil 
sudo apt install -y pssh
sudo apt install -y python3-numpy
sudo apt install -y python3-pandas
sudo apt install -y chrony
sudo systemctl start chronyd
sudo apt install -y firewalld
sudo systemctl enable firewalld
sudo systemctl start firewalld
sudo firewall-cmd --add-service=ntp --permanent
sudo firewall-cmd --reload
