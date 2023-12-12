import os
from settings import *
import socket
import netifaces as ni
# Using readlines()

def my_ip():
    hostname = socket.gethostname()
    IPAddr = socket.gethostbyname(hostname)
    print(IPAddr)
    IPAddr= ni.ifaddresses(INTERFACE)[ni.AF_INET][0]['addr']
    print("Your Computer Name is:" + hostname)
    print("Your Computer IP Address is:" + IPAddr)
    return IPAddr

def find_all_ips():
    IPAddr= my_ip()


    secs=IPAddr.split(".")
    netId= ""
    for i in range(len(secs)-1):
        netId+= secs[i]+"."
    netId+="0"
    print(netId)
    print("finding online ips")
    os.system("nmap -n -sn "+netId+"/24 -oG - | awk '/Up$/{print $2}' > ips.txt")
    print("ips found")
    # os.system("nmap -n -sn 172.16.59.0/24 -oG - | awk '/Up$/{print $2}' ")


def find_server():
    file1 = open('ips.txt', 'r')
    Lines = file1.readlines()
    
    count = 0

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(FINDER_TIMEOUT)
    line =None
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
            print("server not found  | server finder error")
            print("\n")
            continue
   
    if line:
      
        return line[:-1]
    else:
        return HOST
