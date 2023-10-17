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
                elif recv.type == PLAYER_UPDATE:
                    self.game_state.players[i] = recv.msg
                    connector.playerUpdate(self.game_state)
            except Exception as e:
                print(e)
                client_socket.close()
                del self.game_state.players[i]
                break




        


server = TCPServer()
server.start()

