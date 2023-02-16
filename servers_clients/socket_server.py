import socket
import sys


# run this script on server side using this command python3 socket_server.py port_number 
# example: python3 socket_server.py 6000



def server_program():
    host = '0.0.0.0' #server on local host
    port = int(sys.argv[1])  # pass port no above 1024

    print("Running on host and port:", host, port)


    # Create a TCP/IP socket
    server_socket = socket.socket(socket.AF_INET , socket.SOCK_STREAM)  # get instance

    #The bind() function takes tuple as argument
    server_socket.bind((host, port))  # bind host address and port together

    # configure how many client the server can listen simultaneously
    server_socket.listen(2)
    conn, address = server_socket.accept()  # accept new connection
    print("Connection from: " + str(address))
    while True:
        # receive data stream. it won't accept data packet greater than 1024 bytes
        data = conn.recv(1024).decode()
        if not data:
            # if data is not received break
            break
        print("from connected user: " + str(data))
        conn.send(data.encode())  # send data to the client

    conn.close()  # close the connection

if __name__ == '__main__':
    server_program()