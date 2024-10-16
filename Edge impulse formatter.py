import json
import time
import os

# Example device information (you can customize this based on your actual device)
device_info = {
    "device_name": "none",  # Example MAC address
    "device_type": "Laptop",  # Example device type
    "interval_ms": 32.2588996763754  # Frequency in milliseconds
}

def parse_cleaned_json_to_format(cleaned_file, output_file):
    # Read the cleaned JSON data
    with open(cleaned_file, 'r') as f:
        cleaned_data = json.load(f)

    # Extract data points
    data_points = cleaned_data.get("DataPoints", [])

    # Initialize the output structure
    transformed_data = {
        "protected": {
            "ver": "v1",
            "alg": "none",
            "iat": int(time.time())  # Use current timestamp in seconds since epoch
        },
        "signature": "0000000000000000000000000000000000000000000000000000000000000000",  # Example signature
        "payload": {
            "device_name": device_info["device_name"],
            "device_type": device_info["device_type"],
            "interval_ms": device_info["interval_ms"],
            "sensors": [
                #{ "name": "LapDistance", "units": "m" },
                { "name": "Speed", "units": "m/s" },
                { "name": "BrakePedalPosition", "units": "position" },
                { "name": "ThrottlePedalPosition", "units": "position" },
                { "name": "SteeringInput", "units": "position" },
                { "name": "RearLeft Slip", "units": "ratio" },
                { "name": "RearRight Slip", "units": "ratio" }
            ],
            "values": []
        }
    }

    # Parse the cleaned data points and extract values for each sensor
    for point in data_points:
        player_data = point.get("PlayerData", {})
        car_info = player_data.get("CarInfo", {})

        # Create the sensor values list for each time step
        sensor_values = [
            #player_data.get("LapDistance"),  # LapDistance
            car_info.get("Speed", {}).get("InMs"),  # Speed in m/s
            player_data.get("InputInfo", {}).get("BrakePedalPosition"),  # Brake Pedal Position
            player_data.get("InputInfo", {}).get("ThrottlePedalPosition"),  # Throttle Pedal Position
            player_data.get("InputInfo", {}).get("SteeringInput"),  # Steering Input
            car_info.get("RearLeft", {}).get("Slip"),  # RearLeft Slip
            car_info.get("RearRight", {}).get("Slip")  # RearRight Slip
        ]

        # Append the sensor values to the values array
        transformed_data["payload"]["values"].append(sensor_values)

    # Write the transformed data to the output file
    with open(output_file, 'w') as f:
        json.dump(transformed_data, f, indent=4)

def process_turn_files(input_folder, output_folder):
    # Iterate over all turn files in the input folder
    for root, _, files in os.walk(input_folder):
        for file in files:
            if file.endswith(".json"):
                # Full path of the cleaned JSON file
                cleaned_file = os.path.join(root, file)
                
                # Create corresponding output path
                relative_path = os.path.relpath(cleaned_file, input_folder)
                output_file = os.path.join(output_folder, relative_path)

                # Ensure output directory exists
                os.makedirs(os.path.dirname(output_file), exist_ok=True)

                # Call the parsing function for each file
                parse_cleaned_json_to_format(cleaned_file, output_file)
                print(f"Processed and saved: {output_file}")

# Example usage
input_folder = "Turn data/Conservative"
output_folder = 'Formatted data/Conservative'
os.makedirs(output_folder, exist_ok=True)
process_turn_files(input_folder, output_folder)

# Quick hack to process the aggressive data
input_folder = "Turn data/Agressive"
output_folder = 'Formatted data/Agressive'
os.makedirs(output_folder, exist_ok=True)
process_turn_files(input_folder, output_folder)
