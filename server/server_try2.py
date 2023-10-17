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
            # try:
            # data = client_socket.recv(RECIEVE_BUFFER_SIZE)
            # if not data:  # Checking if data is empty
            #     print("Client disconnected")
            #     client_socket.close()
            #     return CLIENT_CLOSED
            # decoded_data = data.decode("utf-8")
            # if decoded_data == LOGIN_REQ:
            #     response = f"1 2 {i}"
            #     client_socket.send(response.encode("utf-8"))
            #     continue
            # jsondata=json.loads(decoded_data)
            # self.game_state.players[i] = jsondata
            # response = json.dumps(self.game_state.players)
            # client_socket.send(response.encode("utf-8"))

            recv =connector.recieve()
            if recv.type == LOGIN_REQ:
                connector.loginAccepted(self.map_obj)
            elif recv.type == PLAYER_UPDATE:
                self.game_state.players[i] = recv.msg
                connector.playerUpdate(self.game_state)



                # self.revMsg = pickle.loads(data)
                
                # if self.revMsg.type == LOGIN_REQ:
                #     self.loginAccepted()
                # elif self.revMsg.type == PLAYER_UPDATE:
                #     self.playerUpdate()
            # except EOFError:  # Catching the EOFError
            #     print("Client disconnected unexpectedly")
            #     client_socket.close()
            #     return CLIENT_CLOSED

        


server = TCPServer()
server.start()

