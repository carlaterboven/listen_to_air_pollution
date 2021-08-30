import time
from pythonosc.udp_client import SimpleUDPClient

def air_bubbles(pm2_5, client):
    print("air bubbles -> ", pm2_5)

    if pm2_5 < 7:
        client.send_message("/air_bubble", [0, 8837, 400])
        time.sleep(10)
    elif pm2_5 < 15:
        client.send_message("/air_bubble", [0, 8837, 200])
        time.sleep(5)
        client.send_message("/air_bubble", [0, 8837, 200])
        time.sleep(5)
    elif pm2_5 < 28:
        for i in range(4):
            client.send_message("/air_bubble", [0, 8837, 200])
            time.sleep(2.5)
    else:
        for i in range(10):
            client.send_message("/air_bubble", [0, 8837, 200])
            time.sleep(1)
