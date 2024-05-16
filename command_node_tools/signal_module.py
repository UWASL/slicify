import signal

class TimeoutException(Exception):   # Custom exception class
    pass

def timeout_handler(signum, frame):   # Custom signal handler
    raise TimeoutException

# Raise TimeoutException whenever SIGALRM is triggered
def set_timeout_handler():
    signal.signal(signal.SIGALRM, timeout_handler)

