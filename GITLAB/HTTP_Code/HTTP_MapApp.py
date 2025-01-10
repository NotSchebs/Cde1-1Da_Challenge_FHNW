import tkinter as tk
import tkintermapview

class MapApp:
    def __init__(self, width=1200, height=1000, title="Map Viewer"):
        self.root = tk.Tk()
        self.root.geometry(f"{width}x{height}")
        self.root.title(title)
        self.map_widget = tkintermapview.TkinterMapView(self.root, width=width, height=height, corner_radius=0)
        self.map_widget.pack()

    def set_initial_position(self, latitude, longitude, zoom=0):
        self.map_widget.set_position(latitude, longitude, zoom)

    def add_marker(self, latitude, longitude, label):
        self.map_widget.set_marker(latitude, longitude, label)

    def add_path(self, path, color="black"):
        self.map_widget.set_path(path, color=color)

    def run(self):
        self.root.mainloop()
