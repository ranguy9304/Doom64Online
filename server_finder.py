import os
from settings import *
import socket
# Using readlines()

def my_ip():
    hostname = socket.gethostname()
    IPAddr = socket.gethostbyname(hostname)
    print(IPAddr)
    return IPAddr

def find_all_ips():
    hostname = socket.gethostname()
    IPAddr = socket.gethostbyname(hostname)

    
    print("Your Computer Name is:" + hostname)
    print("Your Computer IP Address is:" + IPAddr)
    secs=IPAddr.split(".")
    netId= ""
    for i in range(len(secs)-1):
        netId+= secs[i]+"."
    netId+="0"
    print(netId)

    os.system("nmap -n -sn 172.16.59.0/24 -oG - | awk '/Up$/{print $2}' > ips.txt")


def find_server():
    file1 = open('ips.txt', 'r')
    Lines = file1.readlines()
    
    count = 0

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(FINDER_TIMEOUT)
    # Strips the newline character
    for line in Lines:
        try:
        # print("-"+line[:-1]+"-")
            s.sendto("server?".encode("utf-8"), (line[:-1],SERVER_FINDER_PORT))
            revMsg , cliAddr = s.recvfrom(RECIEVE_BUFFER_SIZE)
            if revMsg:
                print("request -> "+line+ "\nresponse -> " +revMsg.decode())
                break
            # os.system("ping "+line+" "+str(SERVER_FINDER_PORT))
            count += 1
        except Exception as e:
            print(e)
            continue
    return line[:-1]
