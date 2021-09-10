from pms5003 import PMS5003
import pandas as pd
import time
from multiprocessing import Process
import os
from generate_sound import *

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
                # # concept5 (part1)
                # music()
            else:
                # any other time: prepare data and start sonification processes
                pm1 = (pm1/sampling_steps)
                pm2_5 = (pm2_5/sampling_steps)
                pm10 = (pm10/sampling_steps)
                joint_pm2_5 = (joint_pm2_5/sampling_steps)
                joint_pm10 = (joint_pm10/sampling_steps)

                # # concept1
                # p1 = Process(target=breath, args=[pm1])
                # p2 = Process(target=geiger_counter, args=[pm10s, joint_pm10])

                # # concept2
                # p1 = Process(target=breath, args=[pm1])
                # p2 = Process(target=air_bubbles, args=[pm2_5])
                # p3 = Process(target=asthma_inhaler, args=[pm10s, joint_pm10])

                # # concept3
                # p1 = Process(target=wind_chimes, args=[joint_pm2_5, joint_pm10])
                # p2 = Process(target=wind_leaves, args=[joint_pm2_5, joint_pm10])
                # p3 = Process(target=wind, args=[joint_pm2_5, joint_pm10])

                # concept4
                p1 = Process(target=bees, args=[joint_pm2_5])
                p2 = Process(target=birds, args=[joint_pm10])
                p3 = Process(target=bird_alarm, args=[joint_pm2_5, joint_pm10])

                # # concept5 (part2)
                # noise(joint_pm2_5, joint_pm10)

                p1.start()
                p2.start()
                p3.start()


            # reset
            pm1 = 0
            pm2_5 = 0
            pm10 = 0
            joint_pm2_5 = 0
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

                joint_pm2_5 += data.pm_ug_per_m3(2.5)
                joint_pm10 += data.pm_ug_per_m3(10.0)
                pm10s.append(data.pm_ug_per_m3(10.0) - data.pm_ug_per_m3(2.5))

                if time.time() - start_timer > 10:
                # if time.time() - start_timer > 10 and p1.is_alive():
                    break

                if not first_round:
                    if not p1.is_alive() or not p2.is_alive() or not p3.is_alive():
                        break

            if first_round:
                first_round = False
            else:
                p1.join()
                p2.join()
                p3.join()


    except KeyboardInterrupt:
        pass
