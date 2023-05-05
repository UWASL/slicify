import time
import subprocess

start = time.time()
subprocess.run (['python3', 'run_program.py' , '&'])
end = time.time()
elapsed_time = end - start
print(elapsed_time)