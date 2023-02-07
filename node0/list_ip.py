import os, re

full_results = [re.findall('^[\w\?\.]+|(?<=\s)\([\d\.]+\)|(?<=at\s)[\w\:]+', i) for i in os.popen('arp -a')]

ip_addresses_list = []

for l in full_results:
    if ((l[0] != '?') and (l[0]!= 'control')):
        ip_addresses_list.append(l[1])

print(ip_addresses_list)