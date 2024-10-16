import json
import os
from utils import * # get folder import function
import warnings


def clean_json(input_file, output_file):
    # Read the input JSON file
    with open(input_file, 'r') as f:
        data = json.load(f)

    # Initialize a new cleaned structure
    cleaned_data = {
        "LapSummary": {
            "LapTimeSeconds": data.get("LapSummary", {}).get("LapTimeSeconds"),
            "LayoutLength": data.get("LapSummary", {}).get("LayoutLength")
        },
        "DataPoints": []
    }

    # Process the DataPoints list
    for point in data.get("DataPoints", []):
        if point.get("PlayerData", {}.get("CurrentLapValid")) == False:
            warnings.warn(f"Invalid lap detected at {point.get('LapTimeSeconds')} in {input_file}")
            continue

        # Clean the PlayerData and CarInfo fields
        cleaned_point = {
            "LapTimeSeconds": point.get("LapTimeSeconds"),
            "PlayerData": {
                "LapDistance": point.get("PlayerData", {}).get("LapDistance"),
                "CarInfo": {
                    "RearLeft": {
                        "Slip": point.get("PlayerData", {}).get("CarInfo", {}).get("WheelsInfo", {}).get("RearLeft", {}).get("Slip")
                    },
                    "RearRight": {
                        "Slip": point.get("PlayerData", {}).get("CarInfo", {}).get("WheelsInfo", {}).get("RearLeft", {}).get("Slip")
                    },
                    "Acceleration": {
                        "XinMs": point.get("PlayerData", {}).get("CarInfo", {}).get("Acceleration", {}).get("XinMs"),
                        "YinMs": point.get("PlayerData", {}).get("CarInfo", {}).get("Acceleration", {}).get("YinMs"),
                        "ZinMs": point.get("PlayerData", {}).get("CarInfo", {}).get("Acceleration", {}).get("ZinMs")
                    },
                    "Speed": {
                        "InMs": point.get("PlayerData", {}).get("Speed", {}).get("InMs")
                    }
                },
                "InputInfo": {
                    "BrakePedalPosition": point.get("InputInfo", {}).get("BrakePedalPosition"),
                    "ThrottlePedalPosition": point.get("InputInfo", {}).get("ThrottlePedalPosition"),
                    "SteeringInput": point.get("InputInfo", {}).get("SteeringInput")
                }
            }
        }

        # Append the cleaned point to the DataPoints list
        cleaned_data["DataPoints"].append(cleaned_point)

    # Write the cleaned data to the output file
    with open(output_file, 'w') as f:
        json.dump(cleaned_data, f, indent=4)

# Main function to process all files
def process_files(input_folder, output_folder):
    # Find all JSON files in the input folder
    input_files = find_new_json_files(input_folder)

    for input_file in input_files:
        # Generate the output file path by replacing the root folder and adding 'cleaned' to the filename
        relative_path = os.path.relpath(input_file, input_folder)
        session_folder = os.path.dirname(relative_path)
        base_name = os.path.basename(input_file).replace('.json', '_cleaned.json')

        # Create the output folder structure if it doesn't exist
        output_path = os.path.join(output_folder, session_folder)
        os.makedirs(output_path, exist_ok=True)

        # Final output file path
        output_file = os.path.join(output_path, base_name)

        # Clean and write the JSON
        clean_json(input_file, output_file)
        print(f"Processed: {input_file} -> {output_file}")

# Example usage
input_folder = 'Raw data\\Conservative'
output_folder = 'Cleaned data\\Conservative'
process_files(input_folder, output_folder)
process_files("Raw data\Aggressive", "Cleaned data\Agressive")
