import requests
import os

"""This function pull the data from the webapplication (https://fl-17-240.zhdk.cloud.switch.ch/) and returns it in a 2D Array

"""

def fetch_data_webapp_http():
    # Defines the URL from the Webapplication and where the data is placed
    download_url = "https://fl-17-240.zhdk.cloud.switch.ch/files/horw-luzern.csv?path=../data/migros/grp3/horw-luzern.csv"

    # Defines the path where the file should be placed
    save_directory = './grp3/backend/data'
    save_path = os.path.join(save_directory, 'horw-luzern.csv')

    # Performs a get request (get data) with the before defined webapp url and file path
    response = requests.get(download_url)

    # Checks if the get request was successful
    if response.status_code == 200:
        # saves the file in the before defined path
        with open(save_path, 'wb') as f:
            f.write(response.content)
        print(f'File was saved in: {save_path}')
    else:
        print(f'Error! The API get request was not successful. Error code: {response.status_code}')


fetch_data_webapp_http()