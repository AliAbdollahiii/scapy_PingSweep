import ipaddress
import random
from scapy.all import ICMP, IP, TCP, sr1
 
try:
	net = input("Enter an IP Range")
	ipaddress.ip_network(net)
except:
	print("Invalid IP Address")
	sys.exit()

# live host 
addresses = ipaddress.ip_network(net)
counter = 0
 
# Sending ICMP ping request, waiting for response
for host in addresses:
    if (host in (addresses.network_address, addresses.broadcast_address)):
        # Skip broadcast addresses
        continue
 
    resp = sr1(IP(dst=str(host))/ICMP(),timeout=0.5,verbose=0,)
 
    if resp is None:
        print("Host {} is Down".format(host))
    elif (int(resp.getlayer(ICMP).type) == 3 and int(resp.getlayer(ICMP).code) in [1,2,3,9,10,13]):
        print("Host {} is Blocking ICMP".format(host))
    elif int(resp.getlayer(ICMP).type) == 0:
        print("Host {} is Live".format(host))
        counter += 1
 
print(" {} host(s) are online.".format(counter))
