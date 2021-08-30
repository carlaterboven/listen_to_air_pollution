import time
from pythonosc.udp_client import SimpleUDPClient

def geiger_counter(pm10s, joint_pm10, client):
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
