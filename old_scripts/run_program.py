#!/usr/bin/env python3
import command_node_tools.config_files.sut_config as sut_config
import subprocess

run_program_commands = sut_config.run_program_commands
id_rsa_location = sut_config.id_rsa_location

for key in run_program_commands.keys():
    command = run_program_commands[key]
    subprocess.run(['ssh', key ,'&&', command ])
    


