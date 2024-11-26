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
        list: A list of rows, where each row is a list of strings containing the CSV data.
    Raises:
        requests.exceptions.RequestException: If the GET request fails.
    Prints:
        str: A success message if the request is successful.
        str: An error message with the status code if the request fails.
    """
    container_data = []

    # Defines the URL from the Webapplication and where the data is placed
    download_url = "https://fl-17-240.zhdk.cloud.switch.ch/files/horw-luzern.csv?path=../data/migros/grp3/horw-luzern.csv"

    # Performs a get request (get data) with the before defined webapp url and file path
    response = requests.get(download_url, verify=False)

    # Checks if the get request was successful
    if response.status_code == 200:
        lines = response.text.splitlines()

        csv_render_object = csv.reader(lines, delimiter=",")
        for row in csv_render_object:
            container_data.append(row)
        return container_data

    else:
        print(
            f"Error! The API get request was not successful. Error code: {response.status_code}"
        )
