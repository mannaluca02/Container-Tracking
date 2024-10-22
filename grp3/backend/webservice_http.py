
# Import library
import requests
import csv

def fetch_webservice_http(container_id,route_id):

    # Request URL
    url = f'https://fl-17-240.zhdk.cloud.switch.ch/containers/{container_id}/routes/{route_id}?start=0&end=-1&format=csv'
    headers = {'accept': 'text/plain',}

    # Send the GET request
    response = requests.get(url, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:

        # Initialize list
        container_data = []

        # Get the content of the response as text (CSV format)
        csv_data = response.text.splitlines()

        # Convert to 2d array
        csv_render_object = csv.reader(csv_data, delimiter=",")
        for row in csv_render_object:
            container_data.append(row)

        # Output
        return container_data

    # Failed Request
    else:
        print("Failed to retrieve data. Status code: {response.status_code}")



#fetch_webservice_http("frodo","luzern-horw")