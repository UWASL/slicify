import os, re
import subprocess
import user_config
import time

setup_commands = user_config.setup_commands
id_rsa_location = user_config.id_rsa_location


for key in setup_commands.keys():
    command = setup_commands[key]
    subprocess.run(['ssh', key ,'-i', id_rsa_location,'-o','StrictHostKeyChecking=no','&&', command ])
    time.sleep(15)




