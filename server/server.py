import os
import sys
sys.path.insert(0, '/home/ranguy/main/projects/Doom64Online/')
import socket
import json
from render_handels.map import *
from multiprocessing import Process, Manager, Lock
from multiprocessing.managers import BaseManager
from connection_handels.server_classes import *
import random
import pickle
from settings import * 

import socket
import threading

class TCPServer:
    Baseconnector = ServerCon()
    map_obj=Map(None)
    map_obj.get_map()
    game_state=Game_State(map_obj=map_obj)
    i=0
    def __init__(self):
     
        self.clients = {}

    def start(self):
    
        while True:
            conn, addr = self.Baseconnector.acceptCon()  # accept a client connection
            print(f"Connection from {addr}")
            # if addr not in self.clients:
            client_thread = threading.Thread(target=self.handle_client, args=(conn, addr,self.i))
            client_thread.start()
            self.i+=1
            # conn =0
            
        



    def handle_client(self, client_socket, addr,i):
        print(f"Handling client {addr}")
        connector= MultiCliCon(client_socket,addr,i)
       
        while True:

            try:
                recv =connector.recieve()
                if not recv:  # connection is closed by client
                    print(f"Connection closed by {addr}")
                    client_socket.close()
                    del self.game_state.players[i]
                    break
                if recv.type == LOGIN_REQ:
                    connector.loginAccepted(self.map_obj)
                    print(recv.msg + " has joined the game")
                elif recv.type == PLAYER_UPDATE:
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
                client_socket.close()
                del self.game_state.players[i]
                break







server = TCPServer()
server.start()

