iface_name = 'enp6s0f0'
filter_string = 'tcp || udp && ip && tcp port not 443 && udp port not 123'
destination = 'seba@node0:/users/seba/node0/logs'
id_rsa_location = '/users/seba/.ssh/id_rsa'
logs_path = '/users/seba/node0/logs/'
stop_port = 13897
