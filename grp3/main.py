import sys


def backend_selection(backend, path=None):
    if backend == 1:
        print(backend)
    elif backend == 2:
        print(backend)
    elif backend == 3:
        print(backend)
    elif backend == 4:
        print(backend)
    else:
        print("This backend type is not supported")


if __name__ == "__main__":
    try: backend_type = int(sys.argv[1])
    except ValueError:
        print("You have to type a number for choosing the backend type")
        sys.exit()
    try:
        csv_file_path = str(sys.argv[2])
    except ValueError:
        print("You have to type a csv file path")
        sys.exit()
    except IndexError:
        if backend_type == 1:
            print("You have to type in a csv file path if you choose the backend type 1")
            sys.exit()

    csv_file_path = None


    backend_selection(backend_type, csv_file_path)
