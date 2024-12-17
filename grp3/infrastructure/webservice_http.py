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
        list: A list of lists, where each inner list represents a row of the CSV data.
        None: In case of failure or error.
    Example:
        >>> data = fetch_webservice_http('container123', 'route456')
        >>> print(data)
        [['header1', 'header2', ...], ['value1', 'value2', ...], ...]
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
            container_data = list(csv.reader(csv_data, delimiter=","))

            if container_data:  # Ensure data is not empty
                return container_data
            else:
                print("Error: No valid data available for the given container and route.")
                return None

        # Handle HTTP error responses
        error_messages = {
            400: "Bad Request: The server could not understand the request. Check your input parameters.",
            401: "Unauthorized: Authentication failed or missing credentials.",
            403: "Forbidden: You don't have permission to access the requested resource.",
            404: f"Not Found: The resource for container ID {container_id} and route ID {route_id} was not found.",
            500: "Internal Server Error: The server encountered an unexpected condition.",
            503: "Service Unavailable: The server is currently unavailable. Try again later.",
        }

        print(error_messages.get(response.status_code, f"Failed to retrieve data. Status code: {response.status_code}"))
        return None

    # Handle connection-related exceptions
    except requests.exceptions.ConnectionError:
        print("Connection Error: Unable to connect to the server. Please check your internet connection or the server URL.")
        return None
    except requests.exceptions.Timeout:
        print("Timeout Error: The server took too long to respond. Try again later.")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None
