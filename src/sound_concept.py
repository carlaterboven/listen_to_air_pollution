import pandas as pd
from multiprocessing import Process
import os
import time
from generate_sound import *

class SoundConcept():
    def __init__(self, pm1, pm2_5, pm10, joint_pm2_5, joint_pm10, pm10s):
        self.__mode = 0
        self.__pm1 = pm1
        self.__pm2_5 = pm2_5
        self.__pm10 = pm10
        self.__joint_pm2_5 = joint_pm2_5
        self.__joint_pm10 = joint_pm10
        self.__pm10s = pm10s

    def __del__(self):
        pass

    def test1(self, pm1):
        print("Test1, pm1: ", pm1)

    def test2(self, pm10s, joint_pm10):
        print("Test1, pm10s: ", pm10s, " and joint pm10: ", joint_pm10)

    def concepttest(self):
        p1 = {"target": self.test1, "args":[self.__pm1]}
        p2 = {"target": self.test2, "args":[self.__pm10s, self.__joint_pm10]}
        p3 = {"target": self.test2, "args":[self.__pm10s, self.__joint_pm10]}
        return pd.DataFrame({"p1": pd.Series(p1), "p2":pd.Series(p2), "p3":pd.Series(p3)})

    def concept1(self):
        p1 = {"target": breath, "args":[pm1]}
        p2 = {"target": geiger_counter, "args":[pm10s, joint_pm10]}
        return pd.DataFrame({"p1": pd.Series(p1), "p2":pd.Series(p2)})

    def concept2(self):
        p1 = {"target": breath, "args":[pm1]}
        p2 = {"target": air_bubbles, "args":[pm2_5]}
        p3 = {"target": asthma_inhaler, "args":[pm10s, joint_pm10]}
        return pd.DataFrame({"p1": pd.Series(p1), "p2":pd.Series(p2), "p3":pd.Series(p3)})

    def concept3(self):
        p1 = {"target": wind_chimes, "args":[joint_pm2_5, joint_pm10]}
        p2 = {"target": wind_leaves, "args":[joint_pm2_5, joint_pm10]}
        p3 = {"target": wind, "args":[joint_pm2_5, joint_pm10]}
        return pd.DataFrame({"p1": pd.Series(p1), "p2":pd.Series(p2), "p3":pd.Series(p3)})

    def concept4(self):
        p1 = {"target": bees, "args":[joint_pm2_5]}
        p2 = {"target": birds, "args":[joint_pm10]}
        p3 = {"target": bird_alarm, "args":[joint_pm2_5, joint_pm10]}
        return pd.DataFrame({"p1": pd.Series(p1), "p2":pd.Series(p2), "p3":pd.Series(p3)})

    def get_concept(self, mode):
        modeDict = {
            "TEST": self.concepttest,
            "GEIGER": self.concept1,
            "ASTHMA": self.concept2,
            "WIND": self.concept3,
            "BEES": self.concept4
        }
        return modeDict.get(mode, lambda: 'Invalid Mode')()
