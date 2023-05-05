import user_config
import subprocess

clean_up_commands = user_config.clean_up_commands
id_rsa_location = user_config.id_rsa_location

for key in clean_up_commands.keys():
    command = clean_up_commands[key]
    subprocess.run(['ssh', key ,'&&', command ])
    

