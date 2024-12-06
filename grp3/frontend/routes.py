import tkinter as tk
from tkintermapview import TkinterMapView


def get_color(temp):
    return "red" if temp > 29 else "orange" if temp >= 26 else "green"


def show_routes(container_data):
    # Create tkinter window
    root = tk.Tk()
    root.geometry("800x600")
    root.title("Map with Dynamic Line Colors")

    # Create the map widget
    map_widget = TkinterMapView(root, width=800, height=600)
    map_widget.pack(fill="both", expand=True)

    # Set starting position and zoom level
    if container_data:
        first_point = container_data[0]
        map_widget.set_position(first_point["x_coordinate"], first_point["y_coordinate"])
        map_widget.set_zoom(14)

    # Draw paths with color-coded temperature
    for i in range(len(container_data) - 1):
        start = (container_data[i]["x_coordinate"], container_data[i]["y_coordinate"])
        end = (container_data[i + 1]["x_coordinate"], container_data[i + 1]["y_coordinate"])
        color = get_color(container_data[i]["temperature"])
        map_widget.set_path([start, end], color=color, width=7)

    root.mainloop()
