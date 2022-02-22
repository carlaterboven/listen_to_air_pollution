# coding=utf-8
import RPi.GPIO as GPIO
import time
from enum import Enum

GPIO.setmode(GPIO.BCM)

# declare pins of rotary encoder
PIN_CLK = 16
PIN_DT = 7
BUTTON_PIN = 8

GPIO.setup(PIN_CLK, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(PIN_DT, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down = GPIO.PUD_UP)

# initialize
counter = 0
direction = True
# PIN_CLK_LAST = 0
PIN_CLK_LAST = GPIO.input(PIN_CLK)
PIN_CLK_NEW = 0
delayTime = 0.01
# number of steps of the rotary encoder
ROTARYSTEPS = 20

class Concept(Enum):
    TEST = 0
    GEIGER = 1
    ASTHMA = 2
    WIND = 3
    BEES = 4

def get_concept(rotary_position):
    if (rotary_position >= 3 and rotary_position < 8):
        concept = Concept.BEES
    elif (rotary_position >= 8 and rotary_position < 13):
        concept = Concept.WIND
    elif (rotary_position >= 13 and rotary_position < 18):
        concept = Concept.ASTHMA
    else:
        concept = Concept.GEIGER
    return concept

# output function runs if sigal detected
def rotary_output(null):
    global counter
    PIN_CLK_NEW = GPIO.input(PIN_CLK)
    if PIN_CLK_NEW != PIN_CLK_LAST:
        if GPIO.input(PIN_DT) != PIN_CLK_NEW:
            counter += 1
        else:
            counter -= 1

        print("New Position: ", counter)
        print("------------------------------")

        rotary_position = counter%ROTARYSTEPS
        concept = get_concept(rotary_position)

        print("New Concept: ", concept)
        print("--------------------------------")

def counter_reset(null):
    global counter
    print("Reset Position!")
    print("------------------------------")
    counter = 0

# Um einen Debounce direkt zu integrieren, werden die Funktionen zur Ausgabe mittels
# CallBack-Option vom GPIO Python Modul initialisiert
GPIO.add_event_detect(PIN_CLK, GPIO.BOTH, callback=rotary_output, bouncetime=50)
GPIO.add_event_detect(BUTTON_PIN, GPIO.FALLING, callback=counter_reset, bouncetime=50)

print("Rotary-Encoder Test [Press Ctrl+C to exit!]")

try:
        while True:
            time.sleep(delayTime)

except KeyboardInterrupt:
        GPIO.cleanup()
