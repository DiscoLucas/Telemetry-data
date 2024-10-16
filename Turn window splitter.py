import json
import os

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

def process_telemetry_for_turns(input_file, output_folder, turn_start_points):
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

        output_file = os.path.join(output_folder, f"turn_{i+1}_lapdistance_{int(turn_start)}.json")
        with open(output_file, 'w') as f_out:
            json.dump(turn_data, f_out, indent=4)
        print(f"Saved turn {i+1} to {output_file}")

# Example usage
#input_file = 'Cleaned data\\Conservative\\session\\cleaned_file.json'
input_file = "Cleaned data\Conservative\\24-10-15-19-20-Red Bull Ring-Practice-e91d14a8-9737-4b33-be6e-4759dceeb036\\Lucas Mitchell-1--e8608838-f6a9-4c0a-a6b8-5cec6c42fb4f_cleaned.json"
output_folder = 'Turn data\\Conservative\\session'
os.makedirs(output_folder, exist_ok=True)

process_telemetry_for_turns(input_file, output_folder, turn_start_points)
