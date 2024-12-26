import csv
import requests
import warnings
from urllib3.exceptions import InsecureRequestWarning

# Suppress all InsecureRequestWarning warnings globally
warnings.simplefilter("ignore", InsecureRequestWarning)


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
    # Define the URL and headers
    url = f"https://fl-17-240.zhdk.cloud.switch.ch/containers/{container_id}/routes/{route_id}?start=0&end=-1&format=csv"
    headers = {"accept": "text/plain"}

    try:
        # Send the GET request
        response = requests.get(url, headers=headers, verify=False)

        # Check if the request was successful
        if response.status_code == 200:
            csv_data = response.text.splitlines()
            csv_data = list(csv.reader(csv_data, delimiter=","))

        # Convert to 2d array
        container_data = []
        for row in csv_data:
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

    except:
        # Handle connection-related exceptions
        error_messages = {
            400: "Bad Request: The server could not understand the request. Check your input parameters.",
            401: "Unauthorized: Authentication failed or missing credentials.",
            403: "Forbidden: You don't have permission to access the requested resource.",
            404: f"Not Found: The resource for container ID {container_id} and route ID {route_id} was not found.",
            500: "Internal Server Error: The server encountered an unexpected condition.",
            503: "Service Unavailable: The server is currently unavailable. Try again later.",
        }

        print(
            error_messages.get(
                response.status_code,
                f"Failed to retrieve data. Status code: {response.status_code}",
            )
        )
        return None
