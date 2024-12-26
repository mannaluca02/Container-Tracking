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


    # open the csv file
    with open(csv_local_path) as container_csv:
        # create an object that separates the entry's of the csv with  ","
        csv_reader_object = csv.reader(container_csv, delimiter=",")
        # go through every entry in the object
        for row in csv_reader_object:
            # append the row to the list of all container data
            entry = {
                "datetime": row[0],
                "x_coordinate": float(row[1]),
                "y_coordinate": float(row[2]),
                "temperature": float(row[3]),
                "humidity": float(row[4]),
            }
            container_data.append(entry)
        print(container_data)
        return container_data

    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        return None
