import csv

def get_local_data(csv_file):
    """
    Reads container data from a csv file and returns it as a list of dictionaries.

    Args:
        csv_file (str): The path to the csv file containing container data.

    Returns:
        A list of dictionaries, where each dictionary represents one row of the csv file with the following keys:
        - 'datetime' (str): The timestamp of the entry.
        - 'x_coordinate' (float): The X-coordinate of the container.
        - 'y_coordinate' (float): The Y-coordinate of the container.
        - 'temperature' (float): The temperature value.
        - 'humidity' (float): The humidity value.

    Raises:
        FileNotFoundError: If the specified csv file does not exist.
        ValueError: If the data in the csv file is not formatted correctly.
    """

    container_data = []

    # open the csv file
    with open(csv_file) as csv_file_object:
        # create an object that separates the entry's of the csv with  ","
        csv_reader = csv.reader(csv_file_object, delimiter=",")
        # go through every entry in the object
        for row in csv_reader:
            # append the row to the list of all container data
            entry = {
                "datetime": row[0],
                "x_coordinate": float(row[1]),
                "y_coordinate": float(row[2]),
                "temperature": float(row[3]),
                "humidity": float(row[4]),
            }
            container_data.append(entry)
    return container_data
