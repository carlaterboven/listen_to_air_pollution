import time
from pythonosc.udp_client import SimpleUDPClient

def breath(pm1, client):
    print(pm1)
    # most relaxed breath is 10 sec
    # one slow breath is 7 sec
    # fastest breath here is 1 sec
    if pm1 < 15:
        client.send_message("/breath", [0, 336001, 10000])
        time.sleep(10)
    elif pm1 < 21:
        client.send_message("/breath", [0, 336001, 5000])
        time.sleep(5)
        client.send_message("/breath", [0, 336001, 5000])
        time.sleep(5)
    elif pm1 < 31:
        for i in range(4):
            client.send_message("/breath", [0, 336001, 2500])
            time.sleep(2.5)
    else:
        for i in range(10):
            client.send_message("/breath", [0, 336001, 1000])
            time.sleep(1)
