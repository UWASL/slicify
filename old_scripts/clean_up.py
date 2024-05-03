#!/usr/bin/env python3
import command_node_tools.config_files.sut_config as sut_config
import subprocess

clean_up_commands = sut_config.clean_up_commands
id_rsa_location = sut_config.id_rsa_location

for key in clean_up_commands.keys():
    command = clean_up_commands[key]
    subprocess.run(['ssh', key ,'&&', command ])
    

