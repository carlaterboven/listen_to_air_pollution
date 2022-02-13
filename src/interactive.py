# coding=utf-8
import RPi.GPIO as GPIO
from enum import Enum
import pandas as pd
import time
from multiprocessing import Process
import os
from generate_sound import *
from sound_concept import *
import sensor as sensor
import rotary_knob as knob

if __name__ ==  '__main__':
    print("Read and sonify PM data. Change sonification mode with rotary knob. [Press Ctrl+C to exit!]")
    GPIO.setmode(GPIO.BCM)

    rotary = knob.Rotaryknob()
    sensor = sensor.Sensor()

    GPIO.setup(rotary.PIN_CLK, GPIO.IN, pull_up_down = GPIO.PUD_UP)
    GPIO.setup(rotary.PIN_DT, GPIO.IN, pull_up_down = GPIO.PUD_UP)
    GPIO.setup(rotary.BUTTON_PIN, GPIO.IN, pull_up_down = GPIO.PUD_UP)

    rotary.set_clk_last(GPIO.input(rotary.PIN_CLK))

    # To directly integrate a debounce, the functions for output are initialized by the CallBack-Option of the GPIO Python module
    GPIO.add_event_detect(rotary.PIN_CLK, GPIO.BOTH, callback=rotary.turn_knob, bouncetime=50)
    GPIO.add_event_detect(rotary.BUTTON_PIN, GPIO.FALLING, callback=rotary.counter_reset, bouncetime=50)

    first_round = True
    mode = Mode.BEES
    processes = []

    try:
        while True:
            if first_round:
                # first time: collect data 10s without sonification
                start_sound()
            else:
                # any other time: prepare data and start sonification processes
                sensor.prepare_data()

                # setup processes based on mode
                new_mode = rotary.get_mode()
                if new_mode is not mode:
                    mode = new_mode
                    processes = []
                    print(mode)
                    concept = modeDict.get(mode, lambda: 'Invalid Mode')()
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

                if not first_round:
                    if not p1.is_alive() or not p2.is_alive() or not p3.is_alive():
                        break

            if first_round:
                first_round = False
            else:
                for process in processes:
                    process.join()

    except KeyboardInterrupt:
            GPIO.cleanup()
