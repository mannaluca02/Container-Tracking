import csv
import requests
import warnings
from urllib3.exceptions import InsecureRequestWarning

# Suppress all InsecureRequestWarning warnings globally
warnings.simplefilter("ignore", InsecureRequestWarning)

def fetch_webapp():
    """
    Fetches container data from a specified web application URL.
    Performs a GET request to download a CSV file from a predefined URL.
    If the request is successful, it reads the CSV content and returns it as a list of rows.
    Each row is represented as a list of strings.
    Returns:
        list: A list of rows, where each row is a list of strings containing the CSV data.
        None: If an error occurs or no valid data is retrieved.
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
                container_data.append(row)

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

        print(error_messages.get(response.status_code, f"Error: The API GET request was not successful. Status code: {response.status_code}"))
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
