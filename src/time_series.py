import pandas as pd
import time
from pythonosc.udp_client import SimpleUDPClient
from multiprocessing import Process
import os
from helper.geiger_counter import geiger_counter
from helper.breath import breath
from helper.air_bubbles import air_bubbles
from helper.asthma_inhaler import asthma_inhaler

client = SimpleUDPClient("127.0.0.1", 6666)

dirname = os.path.dirname(__file__)
DATA_FILE = os.path.join(dirname, '../data/ride6.csv')
ride_df = pd.read_csv(DATA_FILE)
sampling_rate = 10


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

            # # version1
            # p1 = Process(target=breath, args=[pm1, client])
            # p2 = Process(target=geiger_counter, args=[pm10s, joint_pm10, client])
            # p1.start()
            # p2.start()
            # p1.join()
            # p2.join()

            # version2
            p1 = Process(target=breath, args=[pm1, client])
            p2 = Process(target=air_bubbles, args=[pm2_5, client])
            p3 = Process(target=asthma_inhaler, args=[pm10s, joint_pm10, client])
            p1.start()
            p2.start()
            p3.start()
            p1.join()
            p2.join()
            p3.join()

            # reset
            pm1 = 0
            pm2_5 = 0
            pm10 = 0
            joint_pm10 = 0
