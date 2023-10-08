import os
import socket
import json
from map import *
import random
import pickle
host = "127.0.0.1"
port = 7000
s = socket.socket()
s.bind((host, port))
s.listen(10)



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

	# def draw_ray_cast(self):
    #     pg.draw.circle(self.game.screen, 'red', (100 * self.x, 100 * self.y), 15)
    #     if self.ray_cast_player_npc():
    #         pg.draw.line(self.game.screen, 'orange', (100 * self.game.player.x, 100 * self.game.player.y),
    #                      (100 * self.x, 100 * self.y), 2)
map_obj=Map(None)
map_obj.get_map()
game_state=Game_State(map_obj=map_obj)
class Player:
	position=[0,0]
	yaw=0
	shoot=False
	health = 100
	def __init__(self,position=[0,0],yaw=0,shoot=False):
		self.position=position
		self.yaw=yaw
		self.shoot=shoot
	def update(self,position=[0,0],yaw=0,shoot=False):
		self.position=position
		self.yaw=yaw
		self.shoot=shoot
	def __str__(self):
		return str(self.__dict__)
	


def handle_client(s, addr, i):
	while True:
		data = s.recv(1024)
		decoded_data = data.decode("utf-8")
		if not decoded_data:
			print("\nconnection with client " + str(i) + " broken\n")
			break
		if decoded_data=="spawn init":
			x_spawn=random.randrange(1,game_state.map_obj.rows-1,1)
			y_spawn=random.randrange(1,game_state.map_obj.cols-1,1)
			msg='{ "x" : '+str(x_spawn)+' ,"y": '+str(y_spawn)+' }'

			encoded_msg=bytes(msg, "utf-8")

			s.send(encoded_msg)		
		else:
		
			player_data=json.loads(decoded_data)
			game_state.players[i].update(player_data["position"],player_data["yaw"],player_data["shoot"])
			if(game_state.players[i].shoot):
				print("player "+str(i)+" shot")
				
			print(game_state.players[i])
			msg=pickle.dumps(game_state)
			# msg='helo'

			# encoded_msg=bytes(msg, "utf-8")

			s.send(encoded_msg)		
			# print(msg)
			# encoded_msg=bytes(msg, "utf-8")
			# self.s.send(encoded_msg)
			
			



def server():
	i = 1
	lim=10
	global game_state
	while i <= lim:
		c, addr = s.accept()
		child_pid = os.fork()
		if child_pid == 0:
			p0=Player()
			game_state.players[i]=p0
			print("\nconnection successful with client " + str(i) + str(addr) + "\n")
			handle_client(c, addr, i)
			lim+=1
			break
		else:
			i+=1

server()