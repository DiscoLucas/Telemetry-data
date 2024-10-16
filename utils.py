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
