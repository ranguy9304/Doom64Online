

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


        