# coding=utf-8
from enum import Enum
import pandas as pd
import time
from multiprocessing import Process
import os
from generate_sound import *
import sensor as sensor
import sound_concept as sound_concept

if __name__ ==  '__main__':
    print("Read and sonify PM data. Change sonification mode with rotary knob. [Press Ctrl+C to exit!]")
    sensor = sensor.Sensor()

    first_round = True
    processes = []

    try:
        while True:
            if first_round:
                # first time: collect data 10s without sonification
                start_sound()
            else:
                # any other time: prepare data and start sonification processes
                sensor.prepare_data()
                sound_concept_object = sound_concept.SoundConcept(sensor.get_pm1(), sensor.get_pm2_5(), sensor.get_pm10(), sensor.get_joint_pm2_5(), sensor.get_joint_pm10(), sensor.get_pm10s())

                # setup processes based on mode
                # TEST = 0; GEIGER = 1; ASTHMA = 2; WIND = 3; BEES = 4
                mode = 2
                concept = sound_concept_object.get_concept(mode.name)
                processes.clear()

                for part in concept:
                    processes.append(Process(target=concept[part].target, args=concept[part].args))
                for process in processes:
                    process.start()

            sensor.reset_data()

            start_timer = time.time()
            while True:
                sensor.read_data()

                if time.time() - start_timer > 10:
                # if time.time() - start_timer > 10 and p1.is_alive():
                    break

#                 if not first_round:
#                     alive = True
#                     for process in processes:
#                         print("alive: ", alive)
#                         alive = alive and process.is_alive()
#                     if not alive:
#                         break

            if first_round:
                first_round = False
            else:
                for process in processes:
                    process.join()

    except KeyboardInterrupt:
            GPIO.cleanup()
