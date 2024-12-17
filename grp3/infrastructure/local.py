import csv
import os
from pathlib import Path  # Import pathlib if you're working with WindowsPath

def get_local_data(csv_local_path):
    # Convert WindowsPath to a string (if it's a Path object)
    if isinstance(csv_local_path, Path):
        csv_local_path = str(csv_local_path)

    # Check if the file exists
    if not os.path.exists(csv_local_path):
        print(f"Error: The file {csv_local_path} does not exist.")
        return None

    # Check if the file has a '.csv' extension
    if not csv_local_path.endswith(".csv"):
        print(f"Error: The file {csv_local_path} is not a CSV file.")
        return None

    # Check if the file is empty
    if os.path.getsize(csv_local_path) == 0:
        print(f"Error: The file {csv_local_path} is empty.")
        return None

    # Create a list to store every entry of the CSV file
    container_data = []

    try:
        # Open the CSV file
        with open(csv_local_path) as container_csv:
            # Create a CSV reader object to parse the file
            csv_reader_object = csv.reader(container_csv, delimiter=",")

            # Go through every entry in the object
            for row in csv_reader_object:

                # Check if the row contains the correct number of columns
                if len(row) != 5:
                    print(f"Error: Row contains an invalid number of columns or uses an incorrect delimiter (',' expected).")

                    return None  # Return None if any row is invalid

                # Append the row to the list of all container data
                container_data.append(row)

        # Return the valid container data
        return container_data

    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        return None
