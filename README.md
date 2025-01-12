# Container-Tracking
This is the home of the container tracking application.
The tracker can 
- read a local csv file and display the route on a 2d streetmap 
- read a csv file from the webapp and display the route on a 2d streetmap
- read a csv file from the webservice and display the route on a 2d streetmap
- auto start the simulator and read out the data live via mqtt an display the humidity and temperature

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
- Create a virtual environment.
  ```shell
  python -m venv ./venv
  ```
- Activate [virtual environment](https://docs.python.org/3/library/venv.html).
  ```shell
  source ./venv/bin/activate
  ```
- Install dependencies.
    ```
    pip install -r requirements.txt
    ```
## Usage
Start with the Help-Message:
python main.py --help


```bash
python -m venv venv
venv\Scripts\activate  
pip install -r requirements.txt
```
Deactivate virtual env
```bash
deactivate
```


