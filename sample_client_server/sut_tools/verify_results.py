#!/usr/bin/env python3
import os, sys

def verify_1waycomms(test_log_dir_path):
    """
        @brief: Verify results of '1WayComms' test
    """
    file_names = os.listdir(test_log_dir_path)

    for file_name in file_names:
        if("server_" in file_name):
            with open (os.path.join(test_log_dir_path, file_name), 'r') as server_log:
                return_value = False

                for line in server_log:
                    if("Received Message" in line and "TestMessage" in line):
                        return_value = True
    
            if(return_value == True):
                print("\tTest successful")
            else:
                print("\tTest failed")
            return return_value


def verify_results():
    test_key = sys.argv[1]
    test_log_dir = sys.argv[2]

    if(test_key == "1WayComms"):
        return verify_1waycomms(test_log_dir)
    

if __name__ == "__main__":
    verify_results()


