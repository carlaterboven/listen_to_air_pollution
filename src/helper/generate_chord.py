import random

def major_chord(root):
    chord = []
    chord.append(root)
    chord.append(root+4)
    chord.append(root+7)
    return chord


def minor_chord(root):
    chord = []
    chord.append(root)
    chord.append(root+3)
    chord.append(root+7)
    if random.randint(0, 1) == 1: # add seventh with a probability of 50%
        chord.append(root+10)


    return chord

def poly_chord(root):
    return major_chord(root) + minor_chord(root+11)

def normalize_pitch(pm1):
    # we want to normalize the pitch to be in the range between 48 (C2) and 84 (C5)
    new_value = ((pm1 - 0) / (86-0)) * (84 - 48) + 48
    return int(new_value)


def generate_chord(pm1, pm2_5, pm10):
    pm1_normalized = normalize_pitch(pm1)
    if(pm2_5<15 or pm10<4):
        chord = major_chord(pm1_normalized)
        return chord
    elif(pm2_5<28 or pm10<9):
        chord = minor_chord(pm1_normalized)
        return chord
    else:
        chord = poly_chord(pm1_normalized)
        for i in range(len(chord)):
            microtonal_shift = round(random.uniform(-1,1),1)
            chord[i]=chord[i]+microtonal_shift
        return chord
        