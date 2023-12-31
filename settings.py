import math
import subprocess
# game settings
# RES = WIDTH, HEIGHT = 860, 540
# RES = WIDTH, HEIGHT = 1920, 1080

out= subprocess.Popen('xrandr | grep "\*" | cut -d" " -f4',shell=True, stdout=subprocess.PIPE).communicate()[0]
out=out.decode("utf-8")
out=out.split("x")
WIDTH=int(out[0])
HEIGHT=int(out[1])
RES = WIDTH, HEIGHT

HALF_WIDTH = WIDTH // 2
HALF_HEIGHT = HEIGHT // 2
FPS = 0

PLAYER_POS = 1.5, 5  # mini_map
PLAYER_ANGLE = 0
PLAYER_SPEED = 0.004
PLAYER_ROT_SPEED = 0.002
PLAYER_SIZE_SCALE = 60
PLAYER_MAX_HEALTH = 100

MOUSE_SENSITIVITY = 0.0001
MOUSE_MAX_REL = 40
MOUSE_BORDER_LEFT = 100
MOUSE_BORDER_RIGHT = WIDTH - MOUSE_BORDER_LEFT

FLOOR_COLOR = (30, 30, 30)

FOV = math.pi / 3
HALF_FOV = FOV / 2
NUM_RAYS = WIDTH // 2
HALF_NUM_RAYS = NUM_RAYS // 2
DELTA_ANGLE = FOV / NUM_RAYS
MAX_DEPTH = 20

SCREEN_DIST = HALF_WIDTH / math.tan(HALF_FOV)
SCALE = WIDTH // NUM_RAYS

TEXTURE_SIZE = 256
HALF_TEXTURE_SIZE = TEXTURE_SIZE // 2

HOST = "127.0.0.1"
PORT = 7000
SERVER_FINDER_PORT = 6999
LOGIN_REQ ="login req"
PLAYER_UPDATE ="player update"
GAME_STATE ="game state"
LOGIN_RES =  "login res"

CLIENT_CLOSED = "client closed"

RECIEVE_BUFFER_SIZE = 4096

GAME_STATE_KEY ="game_state"
UDP_CON_REQ ="udp connection request"
UDP_CON_RES ="udp connection request"

WEAPON_DAMAGE = 50

FINDER_TIMEOUT=0.1

WIFI = 'wlp3s0'
LOOPBACK = 'lo'
ETHERNET_1 = 'enp2s0'
ETHERNET_2 = 'eth0'





INTERFACE = WIFI

