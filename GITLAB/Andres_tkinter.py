import tkinter as tk
import tkintermapview

# Create the main Tkinter window
root = tk.Tk()
root.title("Tkinter Map View Demo")
root.geometry("800x600")  # Set the window size

# Create a TkinterMapView object
map_widget = tkintermapview.TkinterMapView(root, width=800, height=600)
map_widget.pack(padx=5, pady=5)

# Set the initial position of the map (latitude, longitude)
map_widget.set_position(37.7749, -122.4194)  # San Francisco coordinates
map_widget.set_zoom(12)  # Set zoom level (1-18)

# Add a marker at the initial position
map_widget.set_marker(37.7749, -122.4194, text="San Francisco")  # This is the correct usage.

# Add a function to add markers on click
def on_map_click(lat, lon):
    map_widget.set_marker(lat, lon, text="New Marker")
    print(f"Clicked at: {lat}, {lon}")

map_widget.set_marker(33.7749, -176.4194, text="")

# Bind the map click event to the function
map_widget.bind("<Button-1>", lambda event: on_map_click(event.x, event.y))

# Start the Tkinter event loop
root.mainloop()
