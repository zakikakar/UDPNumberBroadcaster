from sense_hat import SenseHat
from time import sleep
import socket
import json

sense = SenseHat()

def setup_udp_socket():
    # Setup UDP socket for broadcasting
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    # Set a timeout so the socket does not block
    # indefinitely when trying to receive data.
    server.settimeout(0.2)

    #server.bind(("", 44444))
    return server

sense.clear()

s = setup_udp_socket()

red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
yellow = (255,255,0)
nothing = (0,0,0)

number = 1


while True:
    data = {
        "n": number
    }

    # Broadcast message to port 64545 via UDP Socket 
    s.sendto((json.dumps(data, default = str)).encode(), ('<broadcast>', 64545)) #Broadcaster her ud til det valgt portnumber.

    sense.show_message(str(number), scroll_speed=0.1, text_colour=yellow, back_colour=blue)

    number+=1
    sleep(1)