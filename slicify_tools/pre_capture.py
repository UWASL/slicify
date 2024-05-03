import subprocess
import config

filter_string = config.filter_string
capture_filter_filename = config.capture_filter_filename
tcp_ports = set()
udp_ports = set()


def get_tcp_open_ports():
 process = subprocess.run(['netstat', '-ant'], capture_output=True)
 report = process.stdout.decode().splitlines()
 for i in report[2:]:
       tcp_ports.add(i.split()[3].split(":")[-1])
 return tcp_ports


def get_udp_open_ports():
 process = subprocess.run(['netstat', '-anu'], capture_output=True)
 report = process.stdout.decode().splitlines()
 for i in report[2:]:
        udp_ports.add(i.split()[3].split(":")[-1])       
 return udp_ports


def generate_capturing_filter():
  global filter_string      
  for port in udp_ports:
        if(port == "*"):
              continue 
        filter_string += ' && udp port not ' + str(port) + ' '

  for port in tcp_ports:
         if(port == "*"):
                 continue 
         filter_string += '&& tcp port not ' + str(port) + ' '
  return filter_string

def write_filter ():
     with open( capture_filter_filename , 'w') as out_file:
          out_file.write("%s\n" % filter_string)

if __name__ == '__main__':
     get_tcp_open_ports()
     get_udp_open_ports()
     generate_capturing_filter()
     write_filter()
     print("Done")