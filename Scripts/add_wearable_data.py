import glob
import json
import pandas as pd
import time
import datetime
from datetime import timezone

sheets = pd.read_csv("ids.csv")
BIOMETRIC_CSV_PATH = "../Biometrics/processed/"

for json_file in glob.glob("*/*.json"):
    with open(json_file, 'r') as f:
        data = json.load(f)

    for activity_timestamp in data["activityTimestamps"]:
        if activity_timestamp["name"] == "Sliders0":
            start = activity_timestamp["enter"]
        if activity_timestamp["name"] == "DASS":
            stop = activity_timestamp["leave"]
    
    room = int(sheets.loc[sheets['ID'] == data["id"]]["Kamer"].values[0])
    date_string = time.strftime('%d_%m_%Y', time.localtime(start/1000))

    chest_folder, left_folder, right_folder = "", "", ""
    for biometric_file in glob.glob(BIOMETRIC_CSV_PATH + date_string + "_*{}".format(room)):
        if "chest" in biometric_file:
            chest_folder = biometric_file
        elif "left" in biometric_file:
            left_folder = biometric_file
        elif "right" in biometric_file:
            right_folder = biometric_file

    if not (chest_folder and left_folder and right_folder):
        continue

    chest_frames = []
    left_frames = []  
    right_frames = []

    for chest_file in glob.glob(chest_folder + "/*.csv"):
        chest_frames.append(pd.read_csv(chest_file))

    for left_file in glob.glob(left_folder + "/*.csv"):
        left_frames.append(pd.read_csv(left_file))
    
    for right_file in glob.glob(right_folder + "/*.csv"):
        right_frames.append(pd.read_csv(right_file))

    chest = pd.concat(chest_frames)
    left = pd.concat(left_frames)
    right = pd.concat(right_frames)

    frames = {"chest": chest, "left" : left, "right" : right}
    for name, frame in frames.items():
        if(frame.shape[0] == 0 or frame.shape[1] == 0): continue
        frame[frame.columns[0]] = frame[frame.columns[0]].map(lambda x: int(datetime.datetime.strptime(x.split('.')[0], "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone.utc).timestamp()) * 1000)
        frame.sort_values(by=[frame.columns[0]], inplace=True)
        frame.rename(columns={'Unnamed: 0': 'time'}, inplace=True)

        # Now find start and stop index of relevant data for this participant
        relevant = frame[(frame[frame.columns[0]] >= start) & (frame[frame.columns[0]] <= stop)]

        participant_dir = "/".join(json_file.split("/")[:-1])

        print("Saving cut out {} data for participant {}".format(name, data["id"]))
        relevant.to_csv(participant_dir + "/" + name + ".csv", index=False)

        