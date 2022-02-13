import pandas as pd
from multiprocessing import Process
import os
from generate_sound import *

modeDict = {
    "Mode.TEST": concepttest,
    "Mode.GEIGER": concept1,
    "Mode.ASTHMA": concept2,
    "Mode.WIND": concept3,
    "Mode.BEES": concept4
}

def test1(pm1):
    print("Test1, pm1: ", pm1)

def test2(pm10s, joint_pm10):
    print("Test1, pm1: ", pm10s, " and joint pm10: ", joint_pm10)

def concepttest():
    p1 = {"target": test1, "args":[pm1]}
    p2 = {"target": test2, "args":[pm10s, joint_pm10]}
    p3 = {"target": test2, "args":[pm10s, joint_pm10]}
    return pd.DataFrame({"p1": pd.Series(p1), "p2":pd.Series(p2), "p3":pd.Series(p3)})

def concept1():
    p1 = {"target": breath, "args":[pm1]}
    p2 = {"target": geiger_counter, "args":[pm10s, joint_pm10]}
    return pd.DataFrame({"p1": pd.Series(p1), "p2":pd.Series(p2)})

def concept2():
    p1 = {"target": breath, "args":[pm1]}
    p2 = {"target": air_bubbles, "args":[pm2_5]}
    p3 = {"target": asthma_inhaler, "args":[pm10s, joint_pm10]}
    return pd.DataFrame({"p1": pd.Series(p1), "p2":pd.Series(p2), "p3":pd.Series(p3)})

def concept3():
    p1 = {"target": wind_chimes, "args":[joint_pm2_5, joint_pm10]}
    p2 = {"target": wind_leaves, "args":[joint_pm2_5, joint_pm10]}
    p3 = {"target": wind, "args":[joint_pm2_5, joint_pm10]}
    return pd.DataFrame({"p1": pd.Series(p1), "p2":pd.Series(p2), "p3":pd.Series(p3)})

def concept4():
    p1 = {"target": bees, "args":[joint_pm2_5]}
    p2 = {"target": birds, "args":[joint_pm10]}
    p3 = {"target": bird_alarm, "args":[joint_pm2_5, joint_pm10]}
    return pd.DataFrame({"p1": pd.Series(p1), "p2":pd.Series(p2), "p3":pd.Series(p3)})
