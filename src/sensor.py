from pms5003 import PMS5003
import pandas as pd
import time
from pythonosc.udp_client import SimpleUDPClient
from multiprocessing import Process
import os

client = SimpleUDPClient("127.0.0.1", 6666)

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

def start_sound():
    # TODO add "start sonification signal"
    pass


if __name__ ==  '__main__':
    print("Read and sonify PM data. Press Ctrl+C to exit!")

    # Configure the PMS5003 for Enviro+
    pms5003 = PMS5003(
        device='/dev/ttyAMA0',
        baudrate=9600,
        # pin_enable=22,
        # pin_reset=27
    )

    first_round = True

    try:
        while True:
            if first_round:
                # first time: collect data 10s without sonification
                start_sound()
            else:
                # any other time: prepare data and start sonification processes
                pm1 = (pm1/sampling_steps)
                pm2_5 = (pm2_5/sampling_steps)
                pm10 = (pm10/sampling_steps)
                joint_pm10 = (joint_pm10/sampling_steps)

                p1 = Process(target=breath, args=[pm1])
                p2 = Process(target=geiger, args=[pm10s, joint_pm10])
                p1.start()
                p2.start()

            # reset
            pm1 = 0
            pm2_5 = 0
            pm10 = 0
            joint_pm10 = 0
            pm10s = []
            sampling_steps = 0

            start_timer = time.time()
            while True:
                data = pms5003.read()
                # print(data)
                sampling_steps += 1

                # subtract smaller particle groups to get disjoint data
                pm1 += data.pm_ug_per_m3(1.0)
                pm2_5 += data.pm_ug_per_m3(2.5) - data.pm_ug_per_m3(1.0)
                pm10 += data.pm_ug_per_m3(10.0) - data.pm_ug_per_m3(2.5)
                joint_pm10 += data.pm_ug_per_m3(10.0)
                pm10s.append(data.pm_ug_per_m3(10.0) - data.pm_ug_per_m3(2.5))

                if time.time() - start_timer > 8:
                # if time.time() - start_timer > 10 and p1.is_alive():
                    break

                if not first_round:
                    if not p1.is_alive() or not p2.is_alive():
                        break

            if first_round:
                first_round = False
            else:
                p1.join()
                p2.join()


    except KeyboardInterrupt:
        pass
