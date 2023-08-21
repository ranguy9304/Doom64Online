import socket
import json
class Cli_updates:
    position=[1,0]
    yaw=0
    shoot=False
    def __init__(self,position=[1,0],yaw=0,shoot=False):
        self.position=position
        self.yaw=yaw
        self.shoot=shoot

    def getJson(self):
        print(self.__dict__)
        return json.dumps(self.__dict__)
def client():
    host="127.0.0.1"
    port=7000
    s=socket.socket()
    s.connect((host, port))
    obj=Cli_updates()
    msg=obj.getJson()

    encoded_msg=bytes(msg, "utf-8")

    s.send(encoded_msg)
    # msg=str(input("\n -> "))
    # encoded_msg=bytes(msg, "utf-8")

client()