import socket
import sys


# run this script on server side using this command python3 socket_server.py host port_number 
# example: python3 socket_server.py 10.10.1.1 6000

def server_program(host, port):
    
    with open("/users/s2udayas/slicify/sample_client_server/sut_logs/server_" + str(port) + ".log", "w") as log_file:
        log_file.write("Running on host and port: " +  host + " " + str(port) + "\n")

        # Create a TCP/IP socket
        server_socket = socket.socket(socket.AF_INET , socket.SOCK_STREAM)  # get instance

        #The bind() function takes tuple as argument
        server_socket.bind((host, port))  # bind host address and port together

        # configure how many clients the server can listen simultaneously
        server_socket.listen(2)
        conn, address = server_socket.accept()  # accept new connection
        log_file.write("Connection from: " + str(address) + "\n")
        
        while True:
            # receive data stream. it won't accept data packet greater than 1024 bytes
            data = conn.recv(1024).decode()
            if not data:
                # if data is not received break
                break
            log_file.write("Received Message: " + str(data) + "\n")

        conn.close()  # close the connection

if __name__ == '__main__':
    server_program(sys.argv[1], int(sys.argv[2]))