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

# s = socket.socket()
# s.bind((HOST, PORT))
# s.listen(10)
# Create a Manager object to manage shared data among processes

# class MyManager(BaseManager):
#     pass

# authkey=b'mysecretkey'
# manager = MyManager(address=('', 50000), authkey=authkey)

manager = Manager()
# Create a Lock object to ensure atomic updates to the game state
lock = Lock()

# Create a shared dictionary to store the game state
shared_game_state = manager.dict()

# Initialize the game state
shared_game_state['players'] = manager.dict()
shared_game_state['running'] = False

map_obj=Map(None)
map_obj.get_map()
game_state=Game_State(map_obj=map_obj)

	
def convert_to_regular_dict(obj):
    dict = {}
    # if isinstance(obj, Manager().dict().__class__):
    # with lock:
    for i,val in obj.items():
        # rev=obj[i]
        # if isinstance(val, Manager().dict().__class__):
        #     dict[i] = convert_to_regular_dict(val)
        # else:
        dict[i] = val
        # if isinstance(obj, Manager().dict().__class__):
        #     return {key: convert_to_regular_dict(value) for key, value in obj.items()}
        # elif isinstance(obj, Manager().list().__class__):
        #     return [convert_to_regular_dict(value) for value in obj]
        # else:
    return dict
    # else: 
    #     return obj

def handle_client(conn, addr, game_state, lock, client_id):
    # try:
         # Initialize a new player in the game state when a new client connects
    
    with lock:
        new_player = DataPlayer()  # Create a new player object
        game_state['players'][client_id] = new_player  # Add the new player to the game state
        print(f"\nConnection successful with client {client_id} {addr}\n")

    while True:
        # print(conn)
        # Receive data from the client
        data = conn.recv(RECIEVE_BUFFER_SIZE)
        if not data:
            break
        
        # Deserialize the received data
        # revMsg = pickle.loads(data) 
        # data = conn.recv(4096)
        decoded_data = data.decode("utf-8")
        # print("4 "+decoded_data)
        # decoded data is in json convert to a dict
        if decoded_data == "login":
                response = f"1 2 {client_id}"
                conn.send(response.encode("utf-8"))
                continue
      
        jsondata=json.loads(decoded_data)
        with lock:
            # print(jsondata["position"],jsondata["yaw"],jsondata["shoot"])
            # game_state['players'][client_id]= (jsondata["position"],jsondata["yaw"],jsondata["shoot"])
            # print(game_state['players'])
            # print("################  -> "+str(client_id)+" <-")
            # # for i,val in shared_game_state['players'].items():
            # #     print(val)
            # ress=game_state['players'].copy()
            # print(ress)
            # print("################    <-")
            game_state['players'][client_id] = jsondata
            response = json.dumps(convert_to_regular_dict(game_state['players']))
            conn.send(response.encode("utf-8"))


            # regular_dict = dict(game_state)
            
            # msg ='{"position": [[6, 7]], "yaw": 6.095185307179588, "shoot": false}'
            # ress=convert_to_regular_dict(shared_game_state['players'])
            # print(ress)
            # msg=json.dumps(ress)
            # # print(str(client_id) + "---> " +msg)
            # encoded_msg=bytes(msg, "utf-8")

            # conn.send(encoded_msg)

            # TODO: Update the game state based on the received packet
            # print(revMsg.type)  
            # if revMsg.type == LOGIN_REQ:
            #     sendMsg=PacketClass(type=LOGIN_RES)

            #     x_spawn=random.randrange(1,map_obj.rows-1,1)
            #     y_spawn=random.randrange(1,map_obj.cols-1,1)
            #     print(x_spawn,y_spawn)
            #     sendMsg.msg = LoginRes(x_spawn,y_spawn,client_id)

            #     sendMsg = pickle.dumps(sendMsg)

            #     conn.send(sendMsg) 
            # elif revMsg.type == PLAYER_UPDATE:
            #     if client_id not in shared_game_state['players']:
            #         print(f"Player {client_id} not yet added.")
            #         return

            #     shared_game_state['players'][client_id].update(revMsg.msg.position,revMsg.msg.yaw,revMsg.msg.shoot)
            #     # 	print("what " + decoded_data)
            #     # 	player_data=json.loads(decoded_data)
            #     # 	game_state.players[i].update(player_data["position"],player_data["yaw"],player_data["shoot"])
            #     # 	if(game_state.players[i].shoot):
            #     # 		print("player "+str(i)+" shot")
            #     print("################")
            #     # for i in shared_game_state['players']:
            #     #     print(shared_game_state['players'][i])
            #     # self.gameState[GAME_STATE_KEY].show()
            #     print("################")
            #     # print(self.gameState[GAME_STATE_KEY].players[client_id])
            #     ###################################
            #     sendMsg=PacketClass(type=GAME_STATE)
            #     sendMsg.msg=game_state
            #     # self.gameState[GAME_STATE_KEY].show(client_id)
            #     sendMsg = pickle.dumps(sendMsg)
            #     conn.send(sendMsg)
            pass  # Implement this part based on your game's requirements           
        # Serialize the updated game state and send it back to the client
        
            # conn.sendall(pickle.dumps(game_state))
    
    # except Exception as e:
    #     print(f"Error: {e}")    
    # finally:
    #     with lock:
    #         # Remove the player from the game state when the client disconnects
    #         del game_state['players'][client_id]
    #     print(f"Closing connection to {addr}")
    #     conn.close()
    # while True:
    # 	if connector.recieveReq() == CLIENT_CLOSED:
    # 		return

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
	while True:
		conn =0
		conn, addr = Baseconnector.acceptCon()

		# client_id= len(shared_game_state['players'])  # Use the number of connected players as the client ID
		print(f"New connection from {addr}")
		p = Process(target=handle_client, args=(conn, addr, shared_game_state, lock, i))
		p.start()
		print(f"Started process {p.pid} to handle {addr}")
		i+=1
		# c, addr = s.accept()

		# child_pid = os.fork()

		# if child_pid == 0:
		# 	cliConnector = MultiCliCon(c,addr,game_state,i)
		# 	p0=DataPlayer()
		# 	game_state.players[i]=p0
		# 	print("\nconnection successful with client " + str(i) + str(addr) + "\n")
		# 	handle_client(cliConnector, i)
		# 	lim+=1
		# 	break
		# else:
		# 	i+=1

server()


# from connection_handels.msg_classes import DataPlayer  # Import DataPlayer class

# def handle_client(conn, addr, game_state, lock, client_id):
#     try:
#         # Initialize a new player in the game state when a new client connects
#         with lock:
#             new_player = DataPlayer()  # Create a new player object
#             game_state['players'][client_id] = new_player  # Add the new player to the game state
#             print(f"\nConnection successful with client {client_id} {addr}\n")

#         while True:
#             # Receive data from the client
#             data = conn.recv(RECIEVE_BUFFER_SIZE)
#             if not data:
#                 break
            
#             # Deserialize the received data
#             packet = pickle.loads(data)

#             with lock:
#                 # TODO: Update the game state based on the received packet
#                 pass  # Implement this part based on your game's requirements

#             # Serialize the updated game state and send it back to the client
#             conn.sendall(pickle.dumps(game_state))
    
#     except Exception as e:
#         print(f"Error: {e}")

#     finally:
#         with lock:
#             # Remove the player from the game state when the client disconnects
#             del game_state['players'][client_id]
#         print(f"Closing connection to {addr}")
#         conn.close()

# # ... (rest of the code remains the same)

# # Modify this part to pass the client ID to the handle_client function
# while True:
#     # Accept a new client connection
#     conn, addr = s.accept()
#     client_id = len(shared_game_state['players'])  # Use the number of connected players as the client ID
#     print(f"New connection from {addr}")

#     # Create a new process to handle the client
#     p = Process(target=handle_client, args=(conn, addr, shared_game_state, lock, client_id))
#     p.start()

#     print(f"Started process {p.pid} to handle {addr}")