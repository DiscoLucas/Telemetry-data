import json
import os
from utils import *  # Assuming `find_new_json_files` is imported from utils

# Define the LapDistance array where each turn starts
turn_start_points = [300.0, 1150.0, 2000.0, 2470.0, 2910.0, 3318.0, 3880.0]  # The meter points where each turn starts

def find_closest_lap_distance(data_points, target_distance):
    # Find the closest LapDistance to the target_distance
    closest_point = min(data_points, key=lambda point: abs(point["PlayerData"]["LapDistance"] - target_distance))
    return closest_point

def extract_data_window(start_point, data_points, time_window=10):
    # Extract a window of data spanning 10 seconds starting from the closest LapDistance point
    extracted_data = []
    start_time = start_point["LapTimeSeconds"]

    for point in data_points:
        current_time = point["LapTimeSeconds"]
        if current_time >= start_time and current_time <= start_time + time_window:
            extracted_data.append(point)

    return extracted_data

def process_telemetry_for_turns(input_file, lap_number, output_folder, turn_start_points):
    # Read the input JSON file
    with open(input_file, 'r') as f:
        data = json.load(f)

    data_points = data.get("DataPoints", [])

    # Process each turn start point
    for i, turn_start in enumerate(turn_start_points):
        # Find the closest LapDistance point
        closest_point = find_closest_lap_distance(data_points, turn_start)
        
        # Extract a window of 10 seconds from the closest point
        extracted_data = extract_data_window(closest_point, data_points)

        # Save the extracted data to a new JSON file
        turn_data = {
            "LapSummary": data["LapSummary"],
            "DataPoints": extracted_data
        }

        # Naming the file for the turn with the turn number and start point in the lap folder
        turn_file_name = f"T{i+1}_lapdistance_{int(turn_start)}.json"
        output_file = os.path.join(output_folder, f"Lap_{lap_number}", turn_file_name)

        # Ensure the lap folder exists
        os.makedirs(os.path.dirname(output_file), exist_ok=True)

        # Save the file for this turn
        with open(output_file, 'w') as f_out:
            json.dump(turn_data, f_out, indent=4)
        print(f"Saved turn {i+1} of Lap {lap_number} to {output_file}")

# Main function to process all files
def process_files(input_folder, output_folder):
    # Find all JSON files in the input folder
    input_files = find_new_json_files(input_folder)
    lap_count = 1  # Initialize the lap count

    for input_file in input_files:
        # Generate the session folder path
        relative_path = os.path.relpath(input_file, input_folder)
        session_folder = os.path.dirname(relative_path)
        
        # Create the output folder structure if it doesn't exist
        output_path = os.path.join(output_folder, session_folder)
        os.makedirs(output_path, exist_ok=True)

        # Process each lap by iterating through the cleaned data (assuming multiple laps)
        #lap_count = lap_count + 1  # You can dynamically adjust this based on your data structure if needed
        process_telemetry_for_turns(input_file, lap_count, output_path, turn_start_points)

        lap_count += 1  # Increment lap number for each lap processed
        print(lap_count)

# Example usage
input_folder = "Cleaned data/Conservative"
output_folder = 'Turn data/Conservative'
os.makedirs(output_folder, exist_ok=True)
process_files(input_folder, output_folder)
