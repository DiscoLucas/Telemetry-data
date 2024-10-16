import json
import time

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
        "signature": "b0ee0572a1984b93b6bc56e6576e2cbbd6bccd65d0c356e26b31bbc9a48210c6",  # Example signature
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

# Example usage
#cleaned_file = 'Cleaned data\Conservative\\24-10-15-19-20-Red Bull Ring-Practice-e91d14a8-9737-4b33-be6e-4759dceeb036\\Lucas Mitchell-1--e8608838-f6a9-4c0a-a6b8-5cec6c42fb4f_cleaned.json'
cleaned_file = "Turn data\Conservative\session\\turn_1_lapdistance_300.json"
output_file = 'transformed_data.json'

parse_cleaned_json_to_format(cleaned_file, output_file)
