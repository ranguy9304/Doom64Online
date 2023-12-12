import socket
import string
from settings import *
from server_finder import *
IPAddr = my_ip()

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((IPAddr,SERVER_FINDER_PORT))
while(True):
    recvMsg , cliAddr = s.recvfrom(RECIEVE_BUFFER_SIZE)

    if recvMsg.decode() == "server?":
        print("req")

        s.sendto("yes".encode("utf-8"), cliAddr)
