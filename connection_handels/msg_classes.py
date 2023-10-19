from settings import *
import json

class PacketClass:
    type = None
    msg = None
    def __init__(self,type=None,msg=None):
        self.type=type
        self.msg=msg

class LoginResMsg:
	x=0
	y=0
	id=None
	def __init__(self,x,y,id):
		self.x=x
		self.y=y
		self.id=id
	def getJson(self):
		return json.dumps(self.__dict__)

class JsonPacket:
	type=None
	msg=None
	def __init__(self,type=None,msg=None):
		if type :
			# self.type=type
			# self.msg=msg
			self.type=type
		# if msg:
			if self.type!=LOGIN_REQ:
				self.msg=json.loads(msg)
	def loginReq(self):
		self.type=LOGIN_REQ
		self.msg="login"
		return self.getJson()
	def loginRes(self,spawn):
		self.type=LOGIN_RES
		self.msg=spawn.getJson()
		return self.getJson()
	def playerUpdate(self,player):
		self.type=PLAYER_UPDATE
		self.msg=player.getJson()
		return self.getJson()
	def gameStateUpdate(self,game_state):
		self.type=GAME_STATE
		self.msg=game_state.getJson()
		return self.getJson()
	def getJson(self):
		# print(json.dumps(self.__dict__))
		return json.dumps(self.__dict__)

	


class DataPlayer:
	position=[0,0]
	yaw=0
	shoot=False
	health = None
	shotWho=None
	def __init__(self,position=[0,0],yaw=0,shoot=False,health=None,shotWho=None):
		self.position=position
		self.yaw=yaw
		self.shoot=shoot
		self.health=health
		self.shotWho=shotWho
	def update(self,position=[0,0],yaw=0,shoot=False):
		self.position=position
		self.yaw=yaw
		self.shoot=shoot
	def show(self):
		print(self.__dict__)
	def __str__(self):
		return str(self.__dict__)
	def getJson(self):
		# print(self.__dict__)
		return json.dumps(self.__dict__)

