from settings import *


class PacketClass:
    type = None
    msg = None
    def __init__(self,type=None,msg=None):
        self.type=type
        self.msg=msg

class LoginRes:
	x=0
	y=0
	id=None
	def __init__(self,x,y,id):
		self.x=x
		self.y=y
		self.id=id




class DataPlayer:
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
	def show(self):
		print(self.__dict__)
	def __str__(self):
		return str(self.__dict__)

