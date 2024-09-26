import sys
import argparse
from pathlib import Path
from backend import local


def backend_selection(backend, path):
    if backend == 1:
        list_of_data = local.get_local_data(path)
        print(list_of_data)
    elif backend == 2:
        print(backend)
    elif backend == 3:
        print(backend)
    elif backend == 4:
        print(backend)
    else:
        print("This backend type is not supported")


if __name__ == "__main__":
    # Create an argument parser
    parser = argparse.ArgumentParser(description="Select backend type and optionally provide CSV file path.")

    # Add backend type as a required argument
    parser.add_argument('backend_type', type=int, help='The type of backend to select (1, 2, 3, or 4)')

    # Add an optional argument for the CSV file path
    parser.add_argument('csv_file_path', type=Path, nargs='?',
                        help='Path to the CSV file (required for backend type 1)')

    # Parse the arguments
    args = parser.parse_args()

    backend_type = args.backend_type
    csv_file_path = args.csv_file_path

    # Ensure CSV file path is provided for backend type 1
    if backend_type == 1:
        if csv_file_path is None:
            print("Error: You must provide a CSV file path when choosing backend type 1.")
            sys.exit()

        # Check if the CSV file exists
        if not csv_file_path.exists() or not csv_file_path.is_file():
            print(f"Error: The file {csv_file_path} does not exist.")
            sys.exit()

    # Call backend_selection with the selected backend and CSV file path
    backend_selection(backend_type, csv_file_path)
