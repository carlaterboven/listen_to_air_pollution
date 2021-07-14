import numpy as np
from numpy import random

# the rhythm can consist of eighth notes (E), quarter notes (Q), half notes (H)
# imagine we have 120 bpm: that is 2 beats per second
# our sequencer steps 1 time every second
# so we have for every data point 2 beats (= one half note) to compose
rhythms = {
    'slow': 'H',
    'medium': ['Q Q', 'Q E E', 'E Q E', 'E E Q'],
    'fast': 'E E E E'
}

times = {
    'H': [1],
    'Q Q': [0.5, 0.5],
    'Q E E': [0.5, 0.25, 0.25],
    'E Q E': [0.25, 0.5, 0.25],
    'E E Q': [0.25, 0.25, 0.5],
    'E E E E': [0.25, 0.25, 0.25, 0.25]
}

def random_prob():
    # generate a random number between 0 and 1
    return random.rand()

# we select boundaries for the data based on the given data of 7 rides in Berlin
# e.g. play most of the time slowly when disjoint_PM10 values are smaller than 7
# this meens the probability for half notes has to be high and smaller for eighth notes
# TODO maybe define functions later instead of magic numbers
def generate_thresholds(data_value):
    if data_value <= 7:
        # high probability for slow (80%), smaller for medium and fast (10% each)
        return [0.8, 0.9]
    elif data_value <= 15:
        return [0.1, 0.9]
    else:
        return [0.1, 0.2]

def get_rhythm(prob, thresholds):
    if prob <= thresholds[0]:
        return rhythms['slow']
    elif prob <= thresholds[1]:
        return rhythms['medium'][random.randint(4)]
    else:
        return rhythms['fast']

def generate_rhythm(value):
    thresholds = generate_thresholds(value)
    prob = random_prob()
    return times[get_rhythm(prob, thresholds)]
