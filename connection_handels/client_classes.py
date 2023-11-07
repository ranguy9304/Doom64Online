

import socket
from settings import *
from connection_handels.msg_classes import *
import pickle


class UDPCon:
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


class ClientCon:
    s=None
    sendMsg = None
    revMsg = None
    def __init__(self):
        self.s = socket.socket()
        self.s.connect((HOST, PORT))
    def login(self):
        self.sendMsg=PacketClass(type=LOGIN_REQ)
        self.sendMsg = pickle.dumps(self.sendMsg)
        self.s.send(self.sendMsg)
        self.revMsg = self.s.recv(RECIEVE_BUFFER_SIZE)
        self.revMsg = pickle.loads(self.revMsg)
        return [self.revMsg.msg.x,self.revMsg.msg.y,self.revMsg.msg.id]
    def playerUpdate(self,obj):
        self.sendMsg=PacketClass(type=PLAYER_UPDATE)
        self.sendMsg.msg = obj
        self.sendMsg = pickle.dumps(self.sendMsg)
        self.s.send(self.sendMsg)
        self.revMsg = self.s.recv(RECIEVE_BUFFER_SIZE)
        self.revMsg = pickle.loads(self.revMsg)
        return self.revMsg.msg

class ClientJsonCon:
    s=None
    sendMsg = None
    revMsg = None
    def __init__(self):
        self.s = socket.socket()
        self.s.connect((HOST, PORT))
    def login(self,username):
        self.sendMsg=JsonPacket()
        self.sendMsg=self.sendMsg.loginReq(username)
        self.s.send(self.sendMsg.encode("utf-8"))

        self.revMsg = self.s.recv(RECIEVE_BUFFER_SIZE)
        self.revMsg = json.loads(self.revMsg)
        self.revMsg=JsonPacket(self.revMsg["type"],self.revMsg["msg"])
        # print([int(self.revMsg.msg['x']),int(self.revMsg.msg['y']),int(self.revMsg.msg['id'])])
        return [int(self.revMsg.msg["x"]),int(self.revMsg.msg["y"]),int(self.revMsg.msg["id"])]
    def playerUpdate(self,player):
        self.sendMsg=JsonPacket()
        self.sendMsg=self.sendMsg.playerUpdate(player)
        self.s.send(self.sendMsg.encode("utf-8"))

        self.revMsg = self.s.recv(RECIEVE_BUFFER_SIZE)
        # print(self.revMsg)
        self.revMsg = json.loads(self.revMsg)
        self.revMsg = JsonPacket(self.revMsg["type"], self.revMsg["msg"])
        return self.revMsg

        