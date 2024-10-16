import os

# Find all new JSON files in the Raw data folder
def find_new_json_files(folder_path):
    # Initialize an empty list to store the file paths
    new_files = []

    # Iterate over all files in the folder
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            # Check if the file is a JSON file
            if file.endswith(".json"):
                # Append the full file path to the list
                new_files.append(os.path.join(root, file))

    return new_files

import json

# Load the JSON data
with open('Turn data\Conservative\session\\turn_1_lapdistance_300.json', 'r') as file:
    data = json.load(file)

# Extract LapTimeSeconds from DataPoints
lap_times = [point['LapTimeSeconds'] for point in data['DataPoints']]

# Calculate differences between consecutive LapTimeSeconds
time_diffs = [t2 - t1 for t1, t2 in zip(lap_times[:-1], lap_times[1:])]

# Compute the average time difference
average_time_diff = sum(time_diffs) / len(time_diffs)

print(f"Average time between data points: {average_time_diff} seconds")