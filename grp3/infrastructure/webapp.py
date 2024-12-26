import csv
import requests
import warnings
from urllib3.exceptions import InsecureRequestWarning

# Suppress all InsecureRequestWarning warnings globally
warnings.simplefilter("ignore", InsecureRequestWarning)


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
    # Define the URL for the web application
    download_url = "https://fl-17-240.zhdk.cloud.switch.ch/files/horw-luzern.csv?path=../data/migros/frodo/horw-luzern.csv"

    try:
        # Send the GET request
        response = requests.get(download_url, verify=False)

        # Check if the request was successful
        if response.status_code == 200:
            lines = response.text.splitlines()

            # Parse the CSV data
            container_data = []
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
            if container_data:  # Ensure data is not empty
                return container_data
            else:
                print("Error: No valid data available in the downloaded CSV.")
                return None

        # Handle specific HTTP status codes
        error_messages = {
            404: "Error: The requested resource could not be found but may be available in the future.",
            500: f"Error: The server encountered an internal error. Response body: {response.text}",
        }

        print(
            error_messages.get(
                response.status_code,
                f"Error: The API GET request was not successful. Status code: {response.status_code}",
            )
        )
        return None

    # Handle connection-related exceptions
    except requests.exceptions.ConnectionError:
        print(
            "Connection Error: Unable to connect to the server. Please check your internet connection or the server URL."
        )
        return None

    except requests.exceptions.Timeout:
        print("Timeout Error: The server took too long to respond. Try again later.")
        return None

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None
