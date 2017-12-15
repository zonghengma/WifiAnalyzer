import os
import sys

from datetime import datetime
from operator import add
import numpy as np
import matplotlib.pyplot as plt
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

association_terms = ["CTRL-EVENT-DRIVER-STATE STARTED",
                     "-> DISCONNECTED",
                     "wlan0: State: DISCONNECTED -> SCANNING",
                     "wlan0:    selected ",
                     "wlan0: Request association",
                     "wlan0: CTRL-EVENT-CONNECTED",
                     "wlan0: State",
                     "wlan0: Request to deauthenticate",
                     " Associated with "]
scan_request_durations = []
scan_request_time = []
request_associated_durations = []
request_associated_time = []
associated_connected_durations = []
associated_connected_time = []
total_durations = []
dis_connect_durations = []
dis_connect_time = []
inter_BSS_duration = []
inter_BSS_time = []
intra_BSS_duration = []
intra_BSS_time = []

wifi_log = open("WifiAnalyzer_log.txt", "r");

fmt = '%H:%M:%S.%f'

gTimestamp = None
scan_timestamp = None
select_timestamp = None
request_timestamp = None
assoc_timestamp = None
connected_timestamp = None
disconnect_timestamp = None

g_datetime_object = None
scan_datetime_object = None
select_datetime_object = None
request_datetime_object = None
assoc_datetime_object = None
connected_datetime_object = None
disconnect_datetime_object = None

gbssid = None
select_bssid = None
request_bssid = None
assoc_bssid = None
connected_bssid = None
disconnect_bssid = None

#wifi_log = open("WifiAnalyzer_log.txt", "r");

state_code = 1 #1 indicates disconnected,#2 indicates scanning,#3 indicates associating

for str in wifi_log.readlines():
    if any(s in str for s in association_terms):
        if ("CTRL-EVENT-DRIVER-STATE STARTED" in str):
            gTimestamp = str.split(" [b]")[0].split(",")[1]  # turn on Wi-Fi
            g_datetime_object = datetime.strptime(gTimestamp, fmt)

        if ("-> DISCONNECTED" in str):
            state_code = 1
            disconnect_timestamp = str.split(" [b]")[0].split(",")[1]
            disconnect_datetime_object = datetime.strptime(disconnect_timestamp, fmt)
            #disconnect_bssid = str.split("Request to deauthenticate - bssid=")[1].split(" pending_bssid")[0]
            #if (gbssid != disconnect_bssid):
                #print("Error: disconnected from unconnected AP")
            print("Disconnected at ", disconnect_timestamp)


        if("wlan0: State: DISCONNECTED -> SCANNING" in str and state_code == 1):
            scan_timestamp = str.split(" [b]")[0].split(",")[1]
            scan_datetime_object = datetime.strptime(scan_timestamp, fmt)
            state_code = 2
            print bcolors.WARNING + "Event starts" + bcolors.ENDC
            print("Start scanning at: ", scan_timestamp)

        if("wlan0: Request association" in str and state_code == 2):
            request_timestamp = str.split(" [b]")[0].split(",")[1]
            request_bssid = str.split(" with ")[1].strip()
            request_datetime_object = datetime.strptime(request_timestamp,fmt)
            print("Request: ", request_bssid, " at ", request_timestamp)
            state_code = 3
            #print("Request: ", request_bssid, " at ", request_timestamp)
            #print("request timestamp: ",datetime_object)

        if ("wlan0: Associated with " in str and state_code == 3):
            previous_was_assoc = True
            assoc_timestamp = str.split(" [b]")[0].split(",")[1]
            assoc_datetime_object = datetime.strptime(assoc_timestamp, fmt)
            assoc_bssid = str.split("Associated with ")[1].strip()
            state_code = 4
            print("Associated: ", assoc_bssid, " at ", assoc_timestamp)

        if ("wlan0: Associated with " in str and state_code == 5):
            previous_was_assoc = True
            assoc_timestamp = str.split(" [b]")[0].split(",")[1]
            assoc_datetime_object = datetime.strptime(assoc_timestamp, fmt)
            assoc_bssid = str.split("Associated with ")[1].strip()
            state_code = 6
            print("intra-BSS Associated: ", assoc_bssid, " at ", assoc_timestamp)

        if("CTRL-EVENT-CONNECTED" in str):
            connected_bssid = str.split(" CTRL-EVENT-CONNECTED - Connection to ")[1].split(" completed")[0]
            connected_timestamp = str.split(" [b]")[0].split(",")[1]
            connected_datetime_object = datetime.strptime(connected_timestamp, fmt)
            gbssid = connected_bssid
            #print("Connected: ", connected_bssid, " at ", connected_timestamp)
            if (state_code == 4):
                duration = request_datetime_object - scan_datetime_object
                scan_request_durations.append(float(duration.total_seconds() * 1000))
                duration = assoc_datetime_object - request_datetime_object
                request_associated_durations.append(float(duration.total_seconds() * 1000))
                duration = connected_datetime_object - assoc_datetime_object
                associated_connected_durations.append(float(duration.total_seconds() * 1000))
                duration = connected_datetime_object - scan_datetime_object
                inter_BSS_duration.append(float(duration.total_seconds() * 1000))
                lapses = scan_datetime_object - g_datetime_object
                inter_BSS_time.append(lapses.total_seconds())
                print("inter-BSS Connected: ", connected_bssid, " at ", connected_timestamp)
            if (state_code == 6):
                duration = connected_datetime_object - assoc_datetime_object
                intra_BSS_duration.append(float(duration.total_seconds() * 1000))
                lapses = assoc_datetime_object - g_datetime_object
                intra_BSS_time.append(lapses.total_seconds())
                print("intra-BSS Connected: ", connected_bssid, " at ", connected_timestamp)
            state_code = 5

recovery_mean = np.mean(inter_BSS_duration)
recovery_median = np.median(inter_BSS_duration)
recovery_std = np.std(inter_BSS_duration)
recovery_max = np.max(inter_BSS_duration)
recovery_min = np.min(inter_BSS_duration)
intra_BSS_mean = np.mean(intra_BSS_duration)
intra_BSS_median = np.median(intra_BSS_duration)
intra_BSS_std = np.std(intra_BSS_duration)
intra_BSS_max = np.max(intra_BSS_duration)
intra_BSS_max = np.min(intra_BSS_duration)
wifi_log.close();