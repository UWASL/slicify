import user_config
import subprocess

run_program_commands = user_config.run_program_commands
id_rsa_location = user_config.id_rsa_location

for key in run_program_commands.keys():
    command = run_program_commands[key]
    subprocess.run(['ssh', key ,'&&', command ])
    


