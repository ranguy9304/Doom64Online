import os
import sys
print(os.getcwd())
sys.path.insert(0, os.getcwd())
import socket
import json
from render_handels.map import *
from multiprocessing import Process, Manager, Lock
from multiprocessing.managers import BaseManager
from connection_handels.server_classes import *
from server_finder import *
import random
import pickle
from settings import * 

import socket
import threading


class UDPMultiCliCon:
    s=None
    sendMsg=None
    recvMsg=None
    cliAddr=None
    # gameState=None
    playerId=None
    host=HOST
    restricted_area = {(i, j) for i in range(10) for j in range(10)}
    def __init__(self,port=None,host=None,i=None,addr = None):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s.settimeout(5.0)
        self.cliAddr = addr
        if host:
            self.host = host
        if port:
            self.s.bind((self.host,port))
        else:
            self.s.bind((self.host, PORT))
        self.playerId=i
    def recieve(self):
        print("data trying")
        data = self.s.recvfrom(RECIEVE_BUFFER_SIZE)[0]
        print("data recieved ")
        self.recvMsg = json.loads(data)
        # print("DATA REC "+self.recvMsg["type"],self.recvMsg["msg"])
        self.recvMsg=JsonPacket(self.recvMsg["type"],self.recvMsg["msg"])
        return self.recvMsg
    def loginAccepted(self,map_obj):
        print("login acc in")
        self.sendMsg=JsonPacket()
        # x_spawn=random.randrange(1,map_obj.rows-1,1)
        # y_spawn=random.randrange(1,map_obj.cols-1,1)
        pos = x, y = random.randrange(map_obj.cols), random.randrange(map_obj.rows)
        while (pos in map_obj.world_map) or (pos in self.restricted_area):
            pos = x, y = random.randrange(map_obj.cols), random.randrange(map_obj.rows)
        # x_spawn=1
        # y_spawn=2
        # print(x_spawn,y_spawn)
        res= LoginResMsg(x,y,self.playerId)
        self.sendMsg=self.sendMsg.loginRes(res)
        print("login in sending "+self.sendMsg)
        self.s.sendto(self.sendMsg.encode("utf-8"),self.cliAddr)

        return
    def playerUpdate(self,game_state):
        self.sendMsg=JsonPacket()
        self.sendMsg=self.sendMsg.gameStateUpdate(game_state)
        self.s.sendto(self.sendMsg.encode("utf-8"),self.cliAddr)

        return


class UDPServerCon:
    s=None
    sendMsg=None
    recvMsg=None
    cliAddr = None
    host = None
    def __init__(self,port=None,host=None):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        if host:
            self.host = host
        if port:
            self.s.bind((self.host,port))
        else:
            self.s.bind((self.host, PORT))
    def accMsg(self):
        self.recvMsg , self.cliAddr = self.s.recvfrom(RECIEVE_BUFFER_SIZE)
        self.recvMsg = json.loads(self.recvMsg)
        print("DATA REC "+self.recvMsg["type"],self.recvMsg["msg"])
        self.recvMsg=JsonPacket(self.recvMsg["type"],self.recvMsg["msg"])
        if self.recvMsg.type != UDP_CON_REQ:
            return None,None
        return self.recvMsg,self.cliAddr

    def sendConnMsg(self,cliPort):
        self.sendMsg=JsonPacket()
        self.sendMsg=self.sendMsg.udpConnRes(cliPort)
        self.s.sendto(self.sendMsg.encode("utf-8"), self.cliAddr)



class UDPServer:
    i=0
    map_obj=Map(None)
    map_obj.get_map()
    game_state=Game_State(map_obj=map_obj)
    i=0
    def __init__(self):
        self.client_handlers = {}
        self.main_connector = UDPServerCon(host=my_ip())
        self.next_available_port = PORT + 1
    def assignPort(self):
        client_port = self.next_available_port
        self.next_available_port += 1
        return client_port

    def start(self):
        print("UDP Server started. Waiting for clients...")
        while True:
            data, addr = self.main_connector.accMsg()

            if data:
                # Assign a new port for this client
                com_port = self.assignPort()
                
                # Start a new thread for this client
                client_thread = threading.Thread(target=self.handle_client, args=(addr, com_port,self.i))
                self.client_handlers[addr] = [client_thread,com_port]
                client_thread.start()
                
                # Inform the client about their unique port
                self.main_connector.sendConnMsg(com_port)
                self.i +=1        

    def handle_client(self, client_addr, com_port,i):
        # Create a new socket for this client
        print(f"Handling client {client_addr}")
        connector = UDPMultiCliCon(com_port,my_ip(),i,client_addr)
        

        while True:
            self.game_state.show()

            try:
                recv =connector.recieve()
                # print(recv)
                # print("something")
                if not recv:  # connection is closed by client
                    print(f"Connection closed by {addr}")
                    connector.s.close()
                    del self.game_state.players[i]
                    break
                if recv.type == LOGIN_REQ:
                    connector.loginAccepted(self.map_obj)
                    print(recv.msg + " has joined the game")
                elif recv.type == PLAYER_UPDATE:
                    # print("-------",str(com_port),recv.msg,"-------")
                    if i in self.game_state.players:
                        self.game_state.players[i]["position"] = recv.msg["position"]
                        self.game_state.players[i]["yaw"] = recv.msg["yaw"]
                        self.game_state.players[i]["shoot"] = recv.msg["shoot"]
                        if int(recv.msg["health"]) == int(self.game_state.players[i]["health"])+1:
                            self.game_state.players[i]["health"] = recv.msg["health"]
                    else:
                        self.game_state.players[i] = recv.msg

                            
                        # self.game_state.players[i] = recv.msg
                    hurtPlayerId= recv.msg["shotWho"]
                    if hurtPlayerId != None:
                        print("SHOT "+str(hurtPlayerId))
                        print("init health : "+str(self.game_state.players[int(hurtPlayerId)]["health"]))
                        self.game_state.players[int(hurtPlayerId)]["health"]=int(self.game_state.players[int(hurtPlayerId)]["health"])-WEAPON_DAMAGE
                        self.game_state.players[i]["shotWho"]=None
                        print(self.game_state.players[int(hurtPlayerId)]["health"])
                    # print(recv.msg)
                    connector.playerUpdate(self.game_state)
            except Exception as e:
                print("exception : "+str(e))
                connector.s.close()
                if i in self.game_state.players:
                    del self.game_state.players[i]
                break
            # Process data

# Usage
SERVER_HOST = '0.0.0.0'
SERVER_PORT = 12345
udp_server = UDPServer()
udp_server.start()


