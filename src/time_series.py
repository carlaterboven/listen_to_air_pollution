import pandas as pd
import time
from pythonosc.udp_client import SimpleUDPClient
from multiprocessing import Process
import os

client = SimpleUDPClient("127.0.0.1", 6666)

dirname = os.path.dirname(__file__)
DATA_FILE = os.path.join(dirname, '../data/ride1.csv')
ride_df = pd.read_csv(DATA_FILE)
sampling_rate = 10

def geiger(pm10s, joint_pm10):
    pm10_EU_threshold = 40
    pm10_WHO_threshold = 20

    for pm10 in pm10s:
        # amount of geiger counts is based on pm 10 (between 0 and 25, all outliers rounded to 25)
        pm10 = round(pm10)
        if pm10 > 25:
            pm10 = 25

        print("geiger counts -> ", pm10)
        print("joint pm10 -> ", joint_pm10)

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

def breath(pm1):
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


if __name__ ==  '__main__':
    pm1 = 0
    pm2_5 = 0
    pm10 = 0
    joint_pm10 = 0

    for index, row in ride_df.iterrows():
        pm1 += row['1.0']
        pm2_5 += row['2.5']
        pm10 += row['10.0']
        joint_pm10 += row['PM10.0']

        if index % sampling_rate == 0 and index>0: # subsample our data and take average of last 10 seconds as value

            pm10s = pd.Series(ride_df.iloc[(index-sampling_rate):index, 18])

            pm1 = (pm1/sampling_rate)
            pm2_5 = (pm2_5/sampling_rate)
            pm10 = (pm10/sampling_rate)
            joint_pm10 = (joint_pm10/sampling_rate)

            p1 = Process(target=breath, args=[pm1])
            p2 = Process(target=geiger, args=[pm10s, joint_pm10])
            p1.start()
            p2.start()
            p1.join()
            p2.join()

            # reset
            pm1 = 0
            pm2_5 = 0
            pm10 = 0
            joint_pm10 = 0
