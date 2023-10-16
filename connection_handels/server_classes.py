
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
		
	def ray_cast_player_npc(self,id):
		if self.players[id].position == self.map_pos:
			return True

		wall_dist_v, wall_dist_h = 0, 0
		player_dist_v, player_dist_h = 0, 0

		ox, oy = self.game.player.pos
		x_map, y_map = self.players[id].position

		ray_angle = self.theta

		sin_a = math.sin(ray_angle)
		cos_a = math.cos(ray_angle)

        # horizontals
		y_hor, dy = (y_map + 1, 1) if sin_a > 0 else (y_map - 1e-6, -1)

		depth_hor = (y_hor - oy) / sin_a
		x_hor = ox + depth_hor * cos_a

		delta_depth = dy / sin_a
		dx = delta_depth * cos_a

		for i in range(MAX_DEPTH):
			tile_hor = int(x_hor), int(y_hor)
			if tile_hor == self.map_pos:
				player_dist_h = depth_hor
				break
			if tile_hor in self.map_obj.world_map:
				wall_dist_h = depth_hor
				break
			x_hor += dx
			y_hor += dy
			depth_hor += delta_depth

        # verticals
		x_vert, dx = (x_map + 1, 1) if cos_a > 0 else (x_map - 1e-6, -1)

		depth_vert = (x_vert - ox) / cos_a
		y_vert = oy + depth_vert * sin_a

		delta_depth = dx / cos_a
		dy = delta_depth * sin_a

		for i in range(MAX_DEPTH):
			tile_vert = int(x_vert), int(y_vert)
			if tile_vert == self.map_pos:
			    player_dist_v = depth_vert
			    break
			if tile_vert in self.map_obj.world_map:
			    wall_dist_v = depth_vert
			    break
			x_vert += dx
			y_vert += dy
			depth_vert += delta_depth

		player_dist = max(player_dist_v, player_dist_h)
		wall_dist = max(wall_dist_v, wall_dist_h)

		if 0 < player_dist < wall_dist or not wall_dist:
		    return True
		return False
	def show(self,id):
		for i, player in self.players.items():
			if i != id:
				print(f"Player {i}: {player}") 
		# for i in self.players:
		# 	i.show()


class MultiCliCon:
	s=None
	sendMsg=None
	revMsg=None
	addr=None
	gameState=None
	playerId=None
	def __init__(self,s,addr,gameState,i):
		self.s=s
		self.addr=addr
		self.gameState=gameState
		self.playerId=i
	def recieveReq(self):
		try:
			data = self.s.recv(RECIEVE_BUFFER_SIZE)
			if not data:  # Checking if data is empty
				print("Client disconnected")
				self.s.close()
				return CLIENT_CLOSED
			self.revMsg = pickle.loads(data)
			print(self.revMsg.type)
			if self.revMsg.type == LOGIN_REQ:
				self.loginAccepted()
			elif self.revMsg.type == PLAYER_UPDATE:
				self.playerUpdate()
		except EOFError:  # Catching the EOFError
			print("Client disconnected unexpectedly")
			self.s.close()
			return CLIENT_CLOSED
	def loginAccepted(self):

		self.sendMsg=PacketClass(type=LOGIN_RES)

		x_spawn=random.randrange(1,self.gameState.map_obj.rows-1,1)
		y_spawn=random.randrange(1,self.gameState.map_obj.cols-1,1)

		self.sendMsg.msg = LoginRes(x_spawn,y_spawn,self.playerId)

		self.sendMsg = pickle.dumps(self.sendMsg)

		self.s.send(self.sendMsg)

		print("SPAWN POINT SENT")

		return 
	def playerUpdate(self):
		self.gameState.players[self.playerId].update(self.revMsg.msg.position,self.revMsg.msg.yaw,self.revMsg.msg.shoot)
		# 	print("what " + decoded_data)
		# 	player_data=json.loads(decoded_data)
		# 	game_state.players[i].update(player_data["position"],player_data["yaw"],player_data["shoot"])
		# 	if(game_state.players[i].shoot):
		# 		print("player "+str(i)+" shot")
				
		# print(self.gameState.players[self.playerId])
		###################################
		self.sendMsg=PacketClass(type=GAME_STATE)
		self.sendMsg.msg=self.gameState
		self.gameState.show(self.playerId)
		self.sendMsg = pickle.dumps(self.sendMsg)
		self.s.send(self.sendMsg)
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
		
	