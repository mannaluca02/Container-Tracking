# Container-Tracking
This is the home of the container tracking application.
The tracker can 
- read a local csv file and display the route on a 2d streetmap 
- read a csv file from the webapp and display the route on a 2d streetmap
- read a csv file from the webservice and display the route on a 2d streetmap
- auto start the simulator and read out the data live via mqtt an display the humidity and temperature in a chart

## Requirements
- Check if `python` 3.10.x and higher is installed:
    ```shell
    python --version
    Python 3.12.8
    ```
- Check if `pip` is installed:
    ```shell
    pip --version
    pip 24.2
    ```
    
## Installation
To run this simulator on your local machine use the following guide:
- Clone the repo.
- Create a virtual environment in the project directory.
  ```shell
  python -m venv ./venv
  ```

- Activate [virtual environment](https://docs.python.org/3/library/venv.html 

With Windows

```shell
.\venv\Scripts\activate
```

With MacOS and Linux

```shell
  source ./venv/bin/activate
```

- Install dependencies.

```
pip install -r requirements.txt
```
- Deactivate virtual env after usage 
```shell
deactivate
```

## Usage
Please refer to the compatibility section below.
Start with the Help-Message:
```shell
python main.py -h
usage: main.py [-h] [-p [CSV_PATH]] [-c [CONTAINER_ID]] [-r [ROUTE_ID]] {1,2,3,4}

This script allows selecting a backend type (1–4) and provides options to supply additional parameters required for the chosen backend.

positional arguments:
  {1,2,3,4}             The backend type to select:
                        1: Local CSV file access (requires --csv_path).
                        2: WebApp data fetching (no additional arguments required).
                        3: HTTP service (requires --container_id and --route_id).
                        4: MQTT service (no additional arguments required).

options:
  -h, --help            show this help message and exit

Backend type 1:
  Arguments for backend type 1 (local csv file access)

  -p [CSV_PATH], --csv_path [CSV_PATH]
                        Path to the local csv file. This is required when backend type 1 is selected.
                        Example: -p ./data/demo.csv

Backend type 3:
  Arguments for backend type 3 (http access)

  -c [CONTAINER_ID], --container_id [CONTAINER_ID]
                        The container ID to fetch data for. Required when backend type 3 is selected.
                        Example: -c 'grp3'
  -r [ROUTE_ID], --route_id [ROUTE_ID]
                        The route ID associated with the container. Required when backend type 3 is selected.
                        Example: -r 'demo'
```
## Compatibility
We have tested the application on multiple Windows and MacOS machines, and all tests were successful. However, we encountered issues on a Mac with an M4 chip. There seems to be a problem with urllib and ssl. The bug is not well documented, and the error message lacks detail. Subsequently, we tested our tool on an M3 chip, where it ran successfully. We tried to fix the bug and even attempted to switch to OpenSSL, but all efforts were unsuccessful. It seems that the bug lies outside the area where we can make changes.


