import requests
import os
import csv

"""This function pull the data from the webapplication (https://fl-17-240.zhdk.cloud.switch.ch/) and returns it in a 2D Array

"""

def fetch_webapp():
    container_data = []

    # Defines the URL from the Webapplication and where the data is placed
    download_url = "https://fl-17-240.zhdk.cloud.switch.ch/files/horw-luzern.csv?path=../data/migros/grp3/horw-luzern.csv"

    # Performs a get request (get data) with the before defined webapp url and file path
    response = requests.get(download_url)

    # Checks if the get request was successful
    if response.status_code == 200:
        print("Executed successfully")
        lines = response.text.splitlines()
        
        csv_render_object = csv.reader(lines, delimiter=",")
        for row in csv_render_object:
            container_data.append(row)
        return container_data
        
    else:
        print(f'Error! The API get request was not successful. Error code: {response.status_code}')
    
