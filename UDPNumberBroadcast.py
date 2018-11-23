from sense_hat import SenseHat
import socket
from datetime import datetime
import json

sense = SenseHat()
timestamp = datetime.now()
delay = 1 # delay i sekunder
state = True # program runs if True

def setup_udp_socket():
    # Setup UDP socket for broadcasting
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    # Set a timeout so the socket does not block
    # indefinitely when trying to receive data.
    server.settimeout(0.2)

    #server.bind(("", 44444))
    return server

def get_sense_data():
    sense_data = {
        'temp': round(sense.get_temperature(), 1),
        'press': round(sense.get_pressure(), 1),
        'hum': round(sense.get_humidity(), 1),
        'date': datetime.now()
    }
    
    return sense_data

# thread check if joystick is pressed
# if joystick is pressed set while to True/False depending on state

# init server
server = setup_udp_socket()


while True:
    # check hvis man har trykket på joystick for at stoppe/starte program (while løkke forneden)
    for e in sense.stick.get_events():
        if e.action == 'pressed' and e.direction == 'middle':
            state = True if state == False else False

    # run program
    while(state):
        data = get_sense_data()
        time = data["date"] - timestamp # træk timestamp fra datetime i data

        # Sæt et delay for hvor ofte den skal læse data (delay = 1 sekund)
        if time.seconds > delay:

            # Convert dictionary to JSON Object (str) and then to bytes
            dataBytes = (json.dumps(data, default=str)).encode()

            # Broadcast message to port 64545 via UDP Socket
            server.sendto(dataBytes, ('<broadcast>', 64545))

            # Show a message on the display
            sense.show_message( "sent", scroll_speed=0.05 )
        
        # check hvis man har trykket på joystick for at stoppe/starte program (while løkke forneden)
        for e in sense.stick.get_events():
            if e.action == 'pressed' and e.direction == 'middle':
                state = True if state == False else False