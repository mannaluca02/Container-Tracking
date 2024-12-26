import argparse
import sys
from pathlib import Path

from frontend import routes
from infrastructure import local, mqtt, webapp, webservice_http

if __name__ == "__main__":
    # Create an argument parser
    parser = argparse.ArgumentParser(
        description="This script allows selecting a backend type (1–4) and provides options "
            "to supply additional parameters required for the chosen backend.",
        formatter_class=argparse.RawTextHelpFormatter  #Adding Raw Format to use /n
    )

    # Add backend type as a required argument
    parser.add_argument(
        "backend_type", type=int, choices=range(1, 5),
        help=(
            "The backend type to select:\n"
            "1: Local CSV file access (requires --csv_path).\n"
            "2: WebApp data fetching (no additional arguments required).\n"
            "3: HTTP service (requires --container_id and --route_id).\n"
            "4: MQTT service (no additional arguments required)."
        ),
    )

    # Add an optional argument for the csv file path
    local_group = parser.add_argument_group(
        "Backend type 1", "Arguments for backend type 1 (local csv file access)"
    )
    local_group.add_argument(
        "-p", "--csv_path", type=Path, nargs="?",
        help=(
            "Path to the local csv file. This is required when backend type 1 is selected.\n"
            "Example: -p ./data/demo.csv"
        ),
    )

    http_group = parser.add_argument_group(
        "Backend type 3", "Arguments for backend type 3 (http access)"
    )
    # Add an optional argument for the container id
    http_group.add_argument(
        "-c", "--container_id", type=str, nargs="?",
        help=(
            "The container ID to fetch data for. Required when backend type 3 is selected.\n"
            "Example: -c 'grp3'"
        ),
    )
    # Add the first optional argument for the container id
    http_group.add_argument(
        "-r", "--route_id", type=str, nargs="?",
        help=(
            "The route ID associated with the container. Required when backend type 3 is selected.\n"
            "Example: -r 'demo'"
        ),
    )

    # Parse the provided command-line arguments
    args = parser.parse_args()
    backend_type = args.backend_type
    csv_path = args.csv_path
    container_id = args.container_id
    route_id = args.route_id


    # Handle Backend Type 1
    if backend_type == 1:
        # Check if the CSV file path is provided
        if csv_path is None:
            print(
                "Error: You must provide a file path to a local CSV file when choosing backend type 1."
            )
            sys.exit()

        # Verify that the specified CSV file exists
        if not csv_path.exists() or not csv_path.is_file():
            print(f"Error: The file {csv_path} does not exist.")
            sys.exit()

        # Process the local CSV data
        local_data = local.get_local_data(csv_path)
        routes.show_routes(local_data)

    # Handle Backend Type 2
    elif backend_type == 2:
        # Fetch and display data from the web application
        webapp_data = webapp.fetch_webapp()
        routes.show_routes(webapp_data)

    # Handle Backend Type 3
    elif backend_type == 3:
        # Ensure both container ID and route ID are provided
        if container_id is None or route_id is None:
            print("Error: You must provide a container ID and route ID.")
            sys.exit()

        # Fetch data from the HTTP web service
        webservice_data = webservice_http.fetch_webservice_http(container_id, route_id)
        routes.show_routes(webservice_data)

    # Handle Backend Type 4
    elif backend_type == 4:
        try:
            # Start the MQTT client and handle incoming messages
            mqtt.mqtt_func()  # This function starts the MQTT client and receives messages.

        except KeyboardInterrupt:
            # Stop the MQTT client loop when a keyboard interrupt occurs
            mqtt.stop_event.set()  # Stops the loop when keyboard interrupt occurs
    # Handle invalid backend types
    else:
        sys.exit("Error: Invalid backend type. Please select 1, 2, 3, or 4.")
