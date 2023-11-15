
import socket
from settings import *
from connection_handels.msg_classes import *
import pickle
import random

class Game_State:
	running=False
	players={}
	# score=0
	map_obj=None

	def __init__(self,running=False,players={},map_obj=None):
		self.running=running
		self.players=players
		self.map_obj=map_obj
	def get_players_json(self,id):
		temp={}
		for i , player in self.players.items():
			temp[str(i)]=str(player.__dict__)
		temp[str(-1)]=str(id)
		return json.dumps(temp,indent=1)
		
	
	def show(self,id =None):
		print("Game State: ###########\n")
		if id:
			for i, player in self.players.items():
				if i != id:
					print(f"Player {i}: {player}") 
		else:
			for i, player in self.players.items():
				
				print(f"Player {i}: {player}")
		print("############\n\n")
		# for i in self.players:
		# 	i.show()
	def getJson(self):
		return json.dumps(self.players)


class MultiCliCon:
	s=None
	sendMsg=None
	recvMsg=None
	addr=None
	# gameState=None
	playerId=None
	restricted_area = {(i, j) for i in range(10) for j in range(10)}
	def __init__(self,s,addr,i):
		self.s=s
		self.addr=addr
		# self.gameState=gameState
		self.playerId=i
	def recieve(self):
		data = self.s.recv(RECIEVE_BUFFER_SIZE)
		self.recvMsg = json.loads(data)
		# print("DATA REC "+self.recvMsg["type"],self.recvMsg["msg"])
		self.recvMsg=JsonPacket(self.recvMsg["type"],self.recvMsg["msg"])
		return self.recvMsg
	def loginAccepted(self,map_obj):
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
		self.s.send(self.sendMsg.encode("utf-8"))

		return
	def playerUpdate(self,game_state):
		self.sendMsg=JsonPacket()
		self.sendMsg=self.sendMsg.gameStateUpdate(game_state)
		self.s.send(self.sendMsg.encode("utf-8"))

		return
	# def recieveReq(self):
	# 	try:
	# 		data = self.s.recv(RECIEVE_BUFFER_SIZE)
	# 		if not data:  # Checking if data is empty
	# 			print("Client disconnected")
	# 			self.s.close()
	# 			return CLIENT_CLOSED
	# 		self.revMsg = pickle.loads(data)
			
	# 		if self.revMsg.type == LOGIN_REQ:
	# 			self.loginAccepted()
	# 		elif self.revMsg.type == PLAYER_UPDATE:
	# 			self.playerUpdate()
	# 	except EOFError:  # Catching the EOFError
	# 		print("Client disconnected unexpectedly")
	# 		self.s.close()
	# 		return CLIENT_CLOSED
	# def loginAccepted(self):

	# 	self.sendMsg=PacketClass(type=LOGIN_RES)

	# 	x_spawn=random.randrange(1,self.gameState[GAME_STATE_KEY].map_obj.rows-1,1)
	# 	y_spawn=random.randrange(1,self.gameState[GAME_STATE_KEY].map_obj.cols-1,1)
	# 	print(x_spawn,y_spawn)
	# 	self.sendMsg.msg = LoginRes(x_spawn,y_spawn,self.playerId)

	# 	self.sendMsg = pickle.dumps(self.sendMsg)

	# 	self.s.send(self.sendMsg)

	# 	print("SPAWN POINT SENT")

	# 	return 
	# def playerUpdate(self):
	# 	if self.playerId not in self.gameState[GAME_STATE_KEY].players:
	# 		print(f"Player {self.playerId} not yet added.")
	# 		return

	# 	self.gameState[GAME_STATE_KEY].players[self.playerId].update(self.revMsg.msg.position,self.revMsg.msg.yaw,self.revMsg.msg.shoot)
	# 	# 	print("what " + decoded_data)
	# 	# 	player_data=json.loads(decoded_data)
	# 	# 	game_state.players[i].update(player_data["position"],player_data["yaw"],player_data["shoot"])
	# 	# 	if(game_state.players[i].shoot):
	# 	# 		print("player "+str(i)+" shot")
	# 	print("################")
	# 	self.gameState[GAME_STATE_KEY].show()
	# 	print("################")
	# 	# print(self.gameState[GAME_STATE_KEY].players[self.playerId])
	# 	###################################
	# 	self.sendMsg=PacketClass(type=GAME_STATE)
	# 	self.sendMsg.msg=self.gameState[GAME_STATE_KEY]
	# 	self.gameState[GAME_STATE_KEY].show(self.playerId)
	# 	self.sendMsg = pickle.dumps(self.sendMsg)
	# 	self.s.send(self.sendMsg)
		# print("GAME STATE SENT")
			# # msg='helo'

			# # encoded_msg=bytes(msg, "utf-8")

				
			# print(msg)
			# encoded_msg=bytes(msg, "utf-8")
			# self.s.send(encoded_msg)




class ServerCon:
	s=None
	sendMsg = None
	revMsg = None
	addr=None
	def __init__(self):
		self.s = socket.socket()
		self.s.bind((HOST, PORT))
		self.s.listen(10)
	def acceptCon(self):
		
		return self.s.accept()
		
	