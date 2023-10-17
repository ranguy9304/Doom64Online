

import socket
from settings import *
from connection_handels.msg_classes import *
import pickle

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
    def login(self):
        self.sendMsg=JsonPacket()
        self.sendMsg=self.sendMsg.loginReq()
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
        self.revMsg = json.loads(self.revMsg)
        self.revMsg = JsonPacket(self.revMsg["type"], self.revMsg["msg"])
        return self.revMsg

        