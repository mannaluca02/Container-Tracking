import time
import tkinter as tk
from tkinter import ttk
from tkintermapview import TkinterMapView

def get_color(temp_vars):
    if temp_vars > 29:
        return "red"
    elif 26 <= temp_vars <= 29:
        return "orange"
    else:
        return "green"

def show_routes(container_data):
    # Extract coordinates and corresponding third variable
    coordinates = [(float(row[1]), float(row[2])) for row in container_data]
    temp_vars = [float(row[3]) for row in container_data]

    # Create tkinter window
    root = tk.Tk()
    root.geometry("800x600")
    root.title("Map with Dynamic Line Colors")

    # Create the map widget
    map_widget = TkinterMapView(root, width=800, height=600)
    map_widget.pack(fill="both", expand=True)

    # Set the starting position on the map (using the first coordinate)
    map_widget.set_position(coordinates[0][0], coordinates[0][1])
    map_widget.set_zoom(14)

    # Loop through each pair of consecutive coordinates and draw a line segment
    for i in range(len(coordinates) - 1):
        start = coordinates[i]
        print(i)
        end = coordinates[i + 1]

        # Get the color for this line segment based on the third variable
        color = get_color(temp_vars[i])

        # Draw the line segment with the determined color
        map_widget.set_path([start, end], color=color, width=7)

    # Start the tkinter loop
    root.mainloop()
