import socket
import config


# Create a TCP/IP socket
sock = socket.socket( socket.AF_INET , socket.SOCK_STREAM)

# Bind the socket to the port
stop_port = config.stop_port
server_address = ('localhost', stop_port)
print('Starting up on {} port {}'.format(*server_address))
sock.bind(('', stop_port))

# Listen for incoming connections
sock.listen(2) 

while (True):
  connection , client_address = sock.accept()
  data = connection.recv(16)
  print('received {!r}'.format(data))
  msg = data.decode()
  if msg == ("STOP"):
    break
connection.close()