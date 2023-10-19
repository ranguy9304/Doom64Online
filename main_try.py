import pygame as pg
import sys
from settings import *
from render_handels.map import *
from player_handels.player import *
from render_handels.raycasting import *
from render_handels.object_renderer import *
from sprite_handels.sprite_object import *
from sprite_handels.object_handler import *
from sprite_handels.weapon import *
from sprite_handels.sound import *
from render_handels.pathfinding import *
# from server.server_classes import *
from connection_handels.client_classes import *
from connection_handels.msg_classes import *
import socket
import json
import pickle

playerId=None
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
    connector=None # SOCKET CONNECTOR
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
        self.connector=s
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
 
        global playerId
        obj=DataPlayer([self.player.pos],self.player.angle,self.player.shot,self.player.health,self.player.shotWho)
        # print("check point 3")
        # print(obj)
        game_state_res=self.connector.playerUpdate(obj)
        # for i in game_state_res.msg:
        #     # print(type(i))
        #     if i != str(playerId):
        #         print(str(i) + " " +str(playerId)+ " -> ")
        #         print(game_state_res.msg[i])
                # remove last outputed line
        print(int(game_state_res.msg[str(playerId)]["health"]),self.player.health)
        if int(game_state_res.msg[str(playerId)]["health"])!=self.player.health:
            print("got shot")
            self.player.health=int(game_state_res.msg[str(playerId)]["health"])
            self.player.get_damage()
          
        
        currPlayerServerUpdate=game_state_res.msg[str(playerId)]
        self.player.shotWho=currPlayerServerUpdate["shotWho"]
        # print("shot : "+str(currPlayerServerUpdate["shotWho"]))
        del game_state_res.msg[str(playerId)]

        self.object_handler.updateGameStateNpc(game_state_res.msg)
        
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


def init_new_game():
    connector = ClientJsonCon()
    print("---Connected to server---")

    # spawn_location = connector.login()
    
    spawn_location = connector.login()
    global playerId 
    playerId= spawn_location[2]
    print("spawn location: ",spawn_location)
    game = Game(connector,spawn_location[0],spawn_location[1])
    # game = Game(1,1)

    game.run()


if __name__ == '__main__':
    # init_new_game()

    connector = ClientJsonCon()
    print("---Connected to server---")

    # spawn_location = connector.login()
    
    spawn_location = connector.login()
    # global playerId 
    playerId= spawn_location[2]
    print("spawn location: ",spawn_location)
    game = Game(connector,spawn_location[0],spawn_location[1])
    # game = Game(1,1)

    game.run()
