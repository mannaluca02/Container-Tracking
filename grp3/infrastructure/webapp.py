import csv
import os

import requests


def fetch_webapp():
    """
    Fetches container data from a specified web application URL.

    This function performs a GET request to download a CSV file from a predefined URL.
    If the request is successful, it reads the CSV content and returns it as a list of rows.
    Each row is represented as a list of strings.
    Returns:
        A list of dictionaries, where each dictionary represents one row of the csv file with the following keys:
        - 'datetime' (str): The timestamp of the entry.
        - 'x_coordinate' (float): The X-coordinate of the container.
        - 'y_coordinate' (float): The Y-coordinate of the container.
        - 'temperature' (float): The temperature value.
        - 'humidity' (float): The humidity value.
    Raises:
        requests.exceptions.RequestException: If the GET request fails.
    Prints:
        str: A success message if the request is successful.
        str: An error message with the status code if the request fails.
    """
    container_data = []

    # Defines the URL from the Webapplication and where the data is placed
    download_url = "https://fl-17-240.zhdk.cloud.switch.ch/files/horw-luzern.csv?path=../data/migros/frodo/horw-luzern.csv"

    # Performs a get request (get data) with the before defined webapp url and file path
    response = requests.get(download_url, verify=False)

    # Checks if the get request was successful
    if response.status_code == 200:
        lines = response.text.splitlines()

        csv_render_object = csv.reader(lines, delimiter=",")
        for row in csv_render_object:
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

    else:
        print(
            f"Error! The API get request was not successful. Error code: {response.status_code}"
        )
