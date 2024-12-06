import csv


def get_local_data(csv_local_path):
    # create list to store every entry of the csv file
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
