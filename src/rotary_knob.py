# coding=utf-8
import RPi.GPIO as GPIO
import time
from enum import Enum

class Concept(Enum):
    TEST = 0
    GEIGER = 1
    ASTHMA = 2
    WIND = 3
    BEES = 4

class Rotaryknob:
    # number of steps of the rotary encoder
    rotarysteps = 20
    # declare pins of rotary encoder
    PIN_CLK = 16
    PIN_DT = 7
    BUTTON_PIN = 8

    def __init__(self):
        self.__concept = Concept()
        self.__counter = 0
        self.__rotary_position = 0
        self.__PIN_CLK_LAST = 0
        self.__PIN_CLK_NEW = 0

    def __del__(self):
        pass

    def get_concept(self):
        if (self.__rotary_position >= 2 and self.__rotary_position < 7):
            self.__concept = Concept.BEES
        elif (rotary_position >= 7 and rotary_position < 12):
            self.__concept = Concept.WIND
        elif (rotary_position >= 12 and rotary_position < 17):
            self.__concept = Concept.ASTHMA
        else:
            self.__concept = Concept.GEIGER
        return self.__concept

    def turn_knob(self):
        self.__PIN_CLK_NEW = GPIO.input(Rotaryknob.PIN_CLK)
        if self.__PIN_CLK_NEW != self.__PIN_CLK_LAST:
            # check if knob is turned clockwise or counterclockwise
            if GPIO.input(Rotaryknob.PIN_DT) != self.__PIN_CLK_NEW:
                self.__counter += 1
            else:
                self.__counter -= 1

            print("New Position: ", self.__counter)

            # match counter to position and concept
            self.__rotary_position = self.__counter%Rotaryknob.rotarysteps
            self.__concept = self.get_concept()

            print("New Concept: ", self.__concept)
            print("------------------------------")

    def counter_reset(self):
        print("Reset Position!")
        print("------------------------------")
        self.__counter = 0

    def set_clk_last(self, clk_input):
        self.__PIN_CLK_LAST = clk_input
