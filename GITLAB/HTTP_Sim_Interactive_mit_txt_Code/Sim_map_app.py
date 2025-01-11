import tkinter as tk
import tkintermapview

class MapApp:
    def __init__(self, width=1200, height=1000, title="Map Viewer"):
        """Initialize the Tkinter window and map widget."""
        self.root = tk.Tk()
        self.root.geometry(f"{width}x{height}")
        self.root.title(title)
        self.map_widget = tkintermapview.TkinterMapView(self.root, width=width, height=height, corner_radius=0)
        self.map_widget.pack()

    def set_initial_position(self, latitude, longitude, zoom=0):
        """Set the map's initial position and zoom level."""
        self.map_widget.set_position(latitude, longitude, zoom)

    def add_marker(self, latitude, longitude, label):
        """Add a marker to the map at the specified coordinates with a label."""
        self.map_widget.set_marker(latitude, longitude, label)

    def add_path(self, path, color="black"):
        """Draw a line path on the map between a sequence of points."""
        self.map_widget.set_path(path, color=color)

    def run(self):
        """Start the Tkinter main loop."""
        self.root.mainloop()
