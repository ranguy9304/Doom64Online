import sys
sys.path.insert(0, '/home/ranguy/main/projects/Doom64Online/')

from connection_handels.client_classes import *
from connection_handels.msg_classes import *
from login import *
import socket
import json
import pickle
# from connection_handels.client_classes import *
from server_finder import *
from time import sleep

class UDPCon2:
    s=None
    sendMsg=None
    revMsg=None
    cliAddr = None
    port = None
    host=HOST
    def __init__(self,host=None,port=None):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s.settimeout(0.5)
        if host:
            self.host=host
    def accMsg(self):
        self.revMsg , self.cliAddr = self.s.recvfrom(RECIEVE_BUFFER_SIZE)
        self.revMsg = json.loads(self.revMsg)
        print("DATA REC "+self.recvMsg["type"],self.recvMsg["msg"])
        self.recvMsg=JsonPacket(self.recvMsg["type"],self.recvMsg["msg"])
        if self.recvMsg.type != UDP_CON_REQ:
            return None,None
        return self.recvMsg,self.cliAddr

    def sendConnMsg(self):
        self.sendMsg=JsonPacket()
        self.sendMsg=self.sendMsg.udpConnReq()
        sent =False
        while not sent:
            try:
                self.s.sendto(self.sendMsg.encode("utf-8"), (self.host,PORT))
                self.revMsg = self.s.recvfrom(RECIEVE_BUFFER_SIZE)[0]
                sent = True
            except Exception as e:

                print(e)
                sent = False
                continue
        self.revMsg = json.loads(self.revMsg)
        print("DATA REC "+self.revMsg["type"],self.revMsg["msg"])
        return int(self.revMsg["msg"])
        # return 7001
    def login(self,username):
        
        print(self.host,self.port)

        self.sendMsg=JsonPacket()
        self.sendMsg=self.sendMsg.loginReq(username)
        sent = False
        while not sent:
            try:
        # sleep(0.5)
                self.s.sendto(self.sendMsg.encode("utf-8"), (self.host,self.port))
            # except timeout of socket
                
        
                self.revMsg = self.s.recvfrom(RECIEVE_BUFFER_SIZE)[0]
                sent = True
            except Exception as e:
                print(e)
                sent = False


        print(self.revMsg)
        self.revMsg = json.loads(self.revMsg)
        self.revMsg=JsonPacket(self.revMsg["type"],self.revMsg["msg"])
        # print([int(self.revMsg.msg['x']),int(self.revMsg.msg['y']),int(self.revMsg.msg['id'])])
        return [int(self.revMsg.msg["x"]),int(self.revMsg.msg["y"]),int(self.revMsg.msg["id"])]
    def playerUpdate(self,player):
        self.sendMsg=JsonPacket()
        self.sendMsg=self.sendMsg.playerUpdate(player)

        sent = False
        while not sent:
            try:

                self.s.sendto(self.sendMsg.encode("utf-8"),(self.host,self.port))
                self.revMsg = self.s.recvfrom(RECIEVE_BUFFER_SIZE)[0]
                sent = True
            except Exception as e:
                print(e)
                sent = False
                continue
        


        print(self.revMsg)
        self.revMsg = json.loads(self.revMsg)
        self.revMsg = JsonPacket(self.revMsg["type"], self.revMsg["msg"])
        return self.revMsg



playerId=0

print("---Connected to server---")
find_all_ips()
host = find_server()
print("rudra",host)
connector = UDPCon2(host=host)
socketnew=connector.sendConnMsg()
connector.port= socketnew
spawn_location= connector.login("rudra")
print(spawn_location)
fileObj = open('data.obj', 'rb')
obj = pickle.load(fileObj)
fileObj.close()
print(obj)
while(1):
    game_state_res=connector.playerUpdate(obj)
    for i in game_state_res.msg:
                # print(type(i))
        if i != str(playerId):
            print(str(i) + " " +str(playerId)+ " -> ")
            print(game_state_res.msg[i])
            # remove last outputed line
        # print(int(game_state_res.msg[str(playerId)]["health"]))
    sleep(0.5)