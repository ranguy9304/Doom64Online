import os
import sys
sys.path.insert(0, '/home/ranguy/main/projects/Doom64Online/')
import socket
import json
from render_handels.map import *
from connection_handels.server_classes import *
import random
import pickle
from settings import * 

# s = socket.socket()
# s.bind((HOST, PORT))
# s.listen(10)


map_obj=Map(None)
map_obj.get_map()
game_state=Game_State(map_obj=map_obj)

	


def handle_client(connector, i):
	while True:
		if connector.recieveReq() == CLIENT_CLOSED:
			return
		# game_state.show()
		# data = s.recv(1024)
		# # decoded_data = data.decode("utf-8")
		# revMsg=pickle.loads(data)
		# print(revMsg.type)




		# data = s.recv(1024)
		# decoded_data = data.decode("utf-8")
		# if not decoded_data:
		# 	print("\nconnection with client " + str(i) + " broken\n")
		# 	break
		# if decoded_data=="spawn init":
		# 	x_spawn=random.randrange(1,game_state.map_obj.rows-1,1)
		# 	y_spawn=random.randrange(1,game_state.map_obj.cols-1,1)
		# 	msg='{ "x" : '+str(x_spawn)+' ,"y": '+str(y_spawn)+' }'

		# 	encoded_msg=bytes(msg, "utf-8")

		# 	s.send(encoded_msg)		
		# else:
		# 	print("what " + decoded_data)
		# 	player_data=json.loads(decoded_data)
		# 	game_state.players[i].update(player_data["position"],player_data["yaw"],player_data["shoot"])
		# 	if(game_state.players[i].shoot):
		# 		print("player "+str(i)+" shot")
				
		# 	print(game_state.players[i])
		###################################
			# msg=pickle.dumps(game_state)
			# # msg='helo'

			# # encoded_msg=bytes(msg, "utf-8")

			# s.send(msg)		
			# print(msg)
			# encoded_msg=bytes(msg, "utf-8")
			# self.s.send(encoded_msg)
			
			



def server():
	i = 1
	lim=10
	Baseconnector = ServerCon()
	global game_state
	while i <= lim:
		c, addr = Baseconnector.acceptCon()
		# c, addr = s.accept()

		child_pid = os.fork()

		if child_pid == 0:
			cliConnector = MultiCliCon(c,addr,game_state,i)
			p0=DataPlayer()
			game_state.players[i]=p0
			print("\nconnection successful with client " + str(i) + str(addr) + "\n")
			handle_client(cliConnector, i)
			lim+=1
			break
		else:
			i+=1

server()