import socket
import sys

# run this script on client side using python3 socket_clinet.py server_ip server_port
# example: python3 socket_client.py 10.10.1.3 6000

def client_program():
    host = sys.argv[1]
    port = int (sys.argv[2])  # socket server port number

    print("Running on host and port:", host, port)

    sock = socket.socket( socket.AF_INET, socket.SOCK_STREAM)
    # Connect the socket to the port where the server is listening
    sock.connect(( host, port))
    # Send a STOP packet to all other nodes 
    sock.sendto( b"Thank YOU", (host, port) )
    sock.close()


if __name__ == '__main__':
    client_program()
