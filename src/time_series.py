import pandas as pd
import time
from multiprocessing import Process
import os
from generate_sound import *

dirname = os.path.dirname(__file__)
DATA_FILE = os.path.join(dirname, '../data/ride4.csv')
ride_df = pd.read_csv(DATA_FILE)
sampling_rate = 10


if __name__ ==  '__main__':
    pm1 = 0
    pm2_5 = 0
    pm10 = 0
    joint_pm2_5 = 0
    joint_pm10 = 0

    for index, row in ride_df.iterrows():
        pm1 += row['1.0']
        pm2_5 += row['2.5']
        pm10 += row['10.0']
        joint_pm2_5 += row['PM2.5']
        joint_pm10 += row['PM10.0']

        if index % sampling_rate == 0 and index>0: # subsample our data and take average of last 10 seconds as value

            pm10s = pd.Series(ride_df.iloc[(index-sampling_rate):index, 18])

            pm1 = (pm1/sampling_rate)
            pm2_5 = (pm2_5/sampling_rate)
            pm10 = (pm10/sampling_rate)
            joint_pm2_5 = (joint_pm2_5/sampling_rate)
            joint_pm10 = (joint_pm10/sampling_rate)

            # # version1
            # p1 = Process(target=breath, args=[pm1])
            # p2 = Process(target=geiger_counter, args=[pm10s, joint_pm10])
            # p1.start()
            # p2.start()
            # p1.join()
            # p2.join()

            # # version2
            p1 = Process(target=breath, args=[pm1])
            p2 = Process(target=air_bubbles, args=[pm2_5])
            p3 = Process(target=asthma_inhaler, args=[pm10s, joint_pm10])
            p1.start()
            p2.start()
            p3.start()
            p1.join()
            p2.join()
            p3.join()

            # # version3
            # p1 = Process(target=wind_chimes, args=[joint_pm2_5, joint_pm10])
            # p2 = Process(target=wind_leaves, args=[joint_pm2_5, joint_pm10])
            # p3 = Process(target=wind, args=[joint_pm2_5, joint_pm10])
            # p1.start()
            # p2.start()
            # p3.start()
            # p1.join()
            # p2.join()
            # p3.join()

            # # version4
            # p1 = Process(target=bees, args=[joint_pm2_5])
            # p2 = Process(target=birds, args=[joint_pm10])
            # p3 = Process(target=bird_alarm, args=[joint_pm2_5, joint_pm10])
            # p1.start()
            # p2.start()
            # p3.start()
            # p1.join()
            # p2.join()
            # p3.join()

            # # version5
            # # first time
            # if index == sampling_rate:
            #     music()
            # # every time depending on data
            # noise(joint_pm2_5, joint_pm10)

            # reset
            pm1 = 0
            pm2_5 = 0
            pm10 = 0
            joint_pm10 = 0
