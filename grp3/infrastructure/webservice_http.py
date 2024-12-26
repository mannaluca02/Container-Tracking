import csv

import requests


def fetch_webservice_http(container_id, route_id):
    """
    Fetches container tracking data from a web service in CSV format.
    Args:
        container_id (str): The ID of the container to fetch data for.
        route_id (str): The ID of the route to fetch data for.
    Returns:
        A list of dictionaries, where each dictionary represents one row of the csv file with the following keys:
        - 'datetime' (str): The timestamp of the entry.
        - 'x_coordinate' (float): The X-coordinate of the container.
        - 'y_coordinate' (float): The Y-coordinate of the container.
        - 'temperature' (float): The temperature value.
        - 'humidity' (float): The humidity value.
    Raises:
        requests.exceptions.RequestException: If the request to the web service fails.
    """

    # Request URL
    url = f"https://fl-17-240.zhdk.cloud.switch.ch/containers/{container_id}/routes/{route_id}?start=0&end=-1&format=csv"
    headers = {
        "accept": "text/plain",
    }

    # Send the GET request
    response = requests.get(url, headers=headers, verify=False)

    # Check if the request was successful
    if response.status_code == 200:
        # Initialize list
        container_data = []

        # Get the content of the response as text (CSV format)
        csv_data = response.text.splitlines()

        # Convert to 2d array
        csv_render_object = csv.reader(csv_data, delimiter=",")
        for row in csv_render_object:
            entry = {
                "datetime": row[0],
                "x_coordinate": float(row[1]),
                "y_coordinate": float(row[2]),
                "temperature": float(row[3]),
                "humidity": float(row[4]),
            }
            container_data.append(entry)

        # Output
        return container_data

    # Failed Request
    else:
        print("Failed to retrieve data. Status code: {response.status_code}")
