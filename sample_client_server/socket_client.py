import socket
import sys

# run this script on client side using python3 socket_clinet.py server_ip server_port
# example: python3 socket_client.py 10.10.1.3 6000

def client_program():
    with open("/users/s2udayas/slicify/sample_client_server/sut_logs/client_" + str(port) + ".log", "w") as log_file:
        host = sys.argv[1]
        port = int (sys.argv[2])  # socket server port number
        msg_sent = b'TestMessage'
        log_file.write("Running on host and port: " + host + " " + str(port))

        sock = socket.socket( socket.AF_INET, socket.SOCK_STREAM)
        # Connect the socket to the port where the server is listening
        sock.connect(( host, port))
        # Send packet to all other nodes 
        sock.sendto( msg_sent , (host, port) )
        sock.close()


if __name__ == '__main__':
    client_program()
