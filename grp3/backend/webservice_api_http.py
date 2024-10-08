
# Import library
import requests

# Variables
container_id = "frodo"
route_id = "luzern-horw"

# Request URL
url = f'https://fl-17-240.zhdk.cloud.switch.ch/containers/{container_id}/routes/{route_id}?start=0&end=-1&format=csv'
headers = {'accept': 'text/plain',}

# Send the GET request
response = requests.get(url, headers=headers)
print(response)

# Check if the request was successful
if response.status_code == 200:

    # Get the content of the response as text (CSV format)
    csv_data = response.text

    # Convert the CSV data into a list of strings
    data_list = csv_data.splitlines()
    print(data_list)

# Failed Request
else:

    print(f"Failed to retrieve data. Status code: {response.status_code}")
