import time
from pythonosc.udp_client import SimpleUDPClient

client = SimpleUDPClient("127.0.0.1", 6666)

pm2_5_EU_threshold = 25
pm2_5_WHO_threshold = 10
pm10_EU_threshold = 40
pm10_WHO_threshold = 20

def start_sound():
    # TODO add introduction to sonification concepts
    pass

def wind_chimes(joint_pm2_5, joint_pm10):
    if joint_pm2_5 <= pm2_5_EU_threshold and joint_pm10 <= pm10_EU_threshold:
        for i in range(9):
            client.send_message("/wind_chimes", [0, 45803, 1039])
            time.sleep(1)
        client.send_message("/wind_chimes", [0, 45803, 1039])


def wind_leaves(joint_pm2_5, joint_pm10):
    if joint_pm2_5 > pm2_5_WHO_threshold or joint_pm10 > pm10_WHO_threshold:
        if joint_pm2_5 <= pm2_5_EU_threshold or joint_pm10 <= pm10_EU_threshold:
            client.send_message("/wind_leaves", [0, 441002, 10000])


def wind(joint_pm2_5, joint_pm10):
    if joint_pm2_5 > pm2_5_EU_threshold or joint_pm10 > pm10_EU_threshold:
        for i in range(3):
            client.send_message("/wind", [0, 110022, 2495])
            time.sleep(2.495)
        client.send_message("/wind", [0, 110022, 2495])


def asthma_inhaler(pm10s, joint_pm10):
    for pm10 in pm10s:
        # times of inhaling asthma spray is based on pm 10 (between 0 and 25, all outliers rounded to 25)
        pm10 = round(pm10)
        if pm10 > 25:
            pm10 = 25

        # set time in seconds while geiger clicks
        sampling_time = 1
        # only click if higher than threshold
        if joint_pm10 <= pm10_WHO_threshold:
            time.sleep(sampling_time)
        else:
            # click once for every 5µg disjoint PM10 pollution
            num_clicks = pm10//5
            if num_clicks == 0:
                time.sleep(sampling_time)
            else:
                for click in range(num_clicks):
                    client.send_message("/asthma", [0, 42889, 893])
                    time.sleep(sampling_time/num_clicks)


def air_bubbles(pm2_5):
    if pm2_5 < 7:
        for i in range(5):
            client.send_message("/air_bubble", [0, 8837, 600])
            time.sleep(2)
    elif pm2_5 < 15:
        for i in range(10):
            client.send_message("/air_bubble", [0, 8837, 500])
            time.sleep(1)
    elif pm2_5 < 28:
        for i in range(20):
            client.send_message("/air_bubble", [0, 8837, 400])
            time.sleep(0.5)
    else:
        for i in range(25):
            client.send_message("/air_bubble", [0, 8837, 400])
            time.sleep(0.4)


def breath(pm1):
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


def geiger_counter(pm10s, joint_pm10):
    for pm10 in pm10s:
        # amount of geiger counts is based on pm 10 (between 0 and 25, all outliers rounded to 25)
        pm10 = round(pm10)
        if pm10 > 25:
            pm10 = 25

        # set time in seconds while geiger clicks
        sampling_time = 1
        # only click if higher than threshold
        if joint_pm10 <= pm10_WHO_threshold:
            time.sleep(sampling_time)
        else:
            # click once for every 2µg disjoint PM10 pollution
            num_clicks = pm10//2
            if num_clicks == 0:
                time.sleep(sampling_time)
            else:
                for click in range(num_clicks):
                    client.send_message("/geiger", [0, 1585, 33])
                    time.sleep(sampling_time/num_clicks)

def music():
    client.send_message("/music", [0, 9176263, 208079])


def noise(joint_pm2_5, joint_pm10):
    # pollution > EU threshold -> always noise
    # pollution between WHO and EU thersholds -> sometimes noise depending on level of pollution
    # min pollution -> no noise
    if joint_pm2_5 > pm2_5_EU_threshold and joint_pm10 > pm10_EU_threshold:
        client.send_message("/noise", [0, 441001, 10000])
        time.sleep(9.5)
    elif joint_pm2_5 > pm2_5_WHO_threshold and joint_pm10 > pm10_WHO_threshold:
        for i in range(2):
            client.send_message("/noise", [0, 35280, 800])
            time.sleep(1)
            client.send_message("/noise", [0, 35280, 800])
            time.sleep(1)
            client.send_message("/noise", [0, 39690, 900])
            time.sleep(1)
            client.send_message("/noise", [0, 35280, 800])
            time.sleep(1)
            client.send_message("/noise", [0, 39690, 900])
            time.sleep(1)
    elif joint_pm2_5 > pm2_5_WHO_threshold or joint_pm10 > pm10_WHO_threshold:
        for i in range(2):
            client.send_message("/noise", [0, 44100, 1000])
            time.sleep(2.5)
            client.send_message("/noise", [0, 22050, 500])
            time.sleep(2.5)
    else:
        time.sleep(10)


def bees(joint_pm2_5):
    if joint_pm2_5 <= pm2_5_EU_threshold:
            client.send_message("/bees", [0, 441004, 10000])


def birds(joint_pm10):
    if joint_pm10 <= pm10_EU_threshold:
            client.send_message("/birds", [0, 220501, 10000])
            time.sleep(5)
            client.send_message("/birds", [0, 220501, 10000])


def bird_alarm(joint_pm2_5, joint_pm10):
    if joint_pm2_5 > pm2_5_EU_threshold or joint_pm10 > pm10_EU_threshold:
        client.send_message("/bird_alarm", [0, 84364, 1760])
    time.sleep(9.5)
