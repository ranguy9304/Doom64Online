import pygame as pg
import sys
from settings import *
from map import *
from player import *
from raycasting import *
from object_renderer import *
from sprite_object import *
from object_handler import *
from weapon import *
from sound import *
from pathfinding import *
import socket
import json
import pickle
class Cli_updates:
    position=[1,0]
    yaw=0
    shoot=False
    def __init__(self,position=[1,0],yaw=0,shoot=False):
        self.position=position
        self.yaw=yaw
        self.shoot=shoot

    def getJson(self):
        # print(self.__dict__)
        return json.dumps(self.__dict__)
class Game:
    s=None # SOCKET CONNECTOR
    def __init__(self,s,x,y):
    # def __init__(self,x,y):

        pg.init()
        pg.mouse.set_visible(False)
        self.screen = pg.display.set_mode(RES)
        pg.event.set_grab(True)
        self.clock = pg.time.Clock()
        self.delta_time = 1
        self.global_trigger = False
        self.global_event = pg.USEREVENT + 0
        pg.time.set_timer(self.global_event, 40)
        self.s=s
        self.new_game(x,y)


    def new_game(self,x,y):
        self.map = Map(self)
        self.player = Player(self,x,y)
        self.object_renderer = ObjectRenderer(self)
        self.raycasting = RayCasting(self)
        self.object_handler = ObjectHandler(self)
        self.weapon = Weapon(self)
        self.sound = Sound(self)
        self.pathfinding = PathFinding(self)
        pg.mixer.music.play(-1)

    def update(self):
        self.player.update()
        self.raycasting.update()
        self.object_handler.update()
        obj=Cli_updates([self.player.map_pos],self.player.angle,self.player.shot)
        msg=obj.getJson()

        encoded_msg=bytes(msg, "utf-8")

        self.s.send(encoded_msg)
        # data = s.recv(1024)
        # decoded_data = data.decode("utf-8")
        # player_data=pickle.loads(data)
        print(decoded_data)
        self.weapon.update()
        pg.display.flip()
        
        self.delta_time = self.clock.tick(FPS)
        pg.display.set_caption(f'{self.clock.get_fps() :.1f}')

    def draw(self):
        # self.screen.fill('black')
        self.object_renderer.draw()
        self.weapon.draw()
        # self.map.draw()
        # self.player.draw()

    def check_events(self):
        self.global_trigger = False
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()
            elif event.type == self.global_event:
                self.global_trigger = True
            self.player.single_fire_event(event)

    def run(self):
        
        while True:
            self.check_events()
            self.update()
            self.draw()


if __name__ == '__main__':
    host="127.0.0.1"
    port=7000
    s=socket.socket()
    print("---Connected to server---")
    s.connect((host, port))
    msg="spawn init"

    encoded_msg=bytes(msg, "utf-8")

    s.send(encoded_msg)
    data = s.recv(1024)
    decoded_data = data.decode("utf-8")
    spawn_location=json.loads(decoded_data)
    print(spawn_location)
    
    # self.player.x=spawn_location["x"]
    # self.player.y=spawn_location["y"]
    game = Game(s,spawn_location["x"],spawn_location["y"])
    # game = Game(1,1)

    game.run()
