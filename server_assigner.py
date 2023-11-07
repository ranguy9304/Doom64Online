import socket
import string
from settings import *
hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)

 
print("Your Computer Name is:" + hostname)
print("Your Computer IP Address is:" + IPAddr)

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((IPAddr,SERVER_FINDER_PORT))
while(True):
    recvMsg , cliAddr = s.recvfrom(RECIEVE_BUFFER_SIZE)

    if recvMsg.decode() == "server?":
        print("req")

        s.sendto("yes".encode("utf-8"), cliAddr)
