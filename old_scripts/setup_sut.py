#!/usr/bin/env python3
import os, re
import subprocess
import command_node_tools.config_files.sut_config as sut_config
import time

# Grab setup commands from configuration file
setup_commands = sut_config.setup_commands
id_rsa_location = sut_config.id_rsa_location


for node_ip in setup_commands.keys():
    command = setup_commands[node_ip]
    subprocess.run(['ssh', node_ip ,'-i', id_rsa_location,'-o','StrictHostKeyChecking=no','&&', command ])
    time.sleep(15)
