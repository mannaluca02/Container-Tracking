import argparse
import sys
from pathlib import Path

from frontend import routes
from infrastructure import local, mqtt, webapp, webservice_http


def backend_selection(backend, path=None, container_id=None, route_id=None):
    if backend == 1: # From local file
        list_of_data = local.get_local_data(path)
        routes.show_routes(list_of_data)
    elif backend == 2: # from webapp
        list_of_data = webapp.fetch_webapp()
        routes.show_routes(list_of_data)
    elif backend == 3:
        list_of_data = webservice_http.fetch_webservice_http(container_id,route_id)
        routes.show_routes(list_of_data)
        # print(list_of_data)
        # print(backend)
    elif backend == 4:
        try:
            mqtt.mqtt_func()  # Diese Funktion startet den MQTT-Client und empfängt Nachrichten
        except KeyboardInterrupt:
            mqtt.stop_event.set()  # Stoppe die Schleife bei Tastendruck
    else:
        print("This backend type is not supported")


if __name__ == "__main__":
    # Create an argument parser
    # TODO Helper text for the arguments
    parser = argparse.ArgumentParser(description="Select backend type and optionally provide CSV file path.")

    # Add backend type as a required argument
    parser.add_argument('backend_type', type=int, help='The type of backend to select (1, 2, 3, or 4)')

    # Add an optional argument for the CSV file path
    parser.add_argument('-p','--csv_file_path', type=Path, nargs='?',
                        help='Path to the CSV file (required for backend type 1)')

    # Add an optional argument for the container id
    parser.add_argument('-c','--container_id', type=str, nargs='?',
                        help='Name of the container (required for backend type 3)')
    # Add the first optional argument for the container id
    parser.add_argument('-r','--route_id', type=str, nargs='?',
                        help='Name of the route (required for backend type 3)')

    # Parse the arguments
    args = parser.parse_args()

    backend_type = args.backend_type
    csv_file_path = args.csv_file_path
    container_id = args.container_id
    route_id = args.route_id

    # Ensure CSV file path is provided for backend type 1
    if backend_type == 1:
        if csv_file_path is None:
            print("Error: You must provide a file path to a local CSV file when choosing backend type 1.")
            sys.exit()

        # Check if the CSV file exists
        if not csv_file_path.exists() or not csv_file_path.is_file():
            print(f"Error: The file {csv_file_path} does not exist.")
            sys.exit()

        # Call backend_selection with the selected backend and CSV file path
        backend_selection(backend_type, path=csv_file_path)

    elif backend_type == 2:
        backend_selection(backend_type)

    elif backend_type == 3:
        if container_id is None or route_id is None:
            print("Error: You must provide a container ID and route ID.")
            sys.exit()

        backend_selection(backend_type, container_id=container_id, route_id=route_id)
