import tkinter as tk
from tkinter import ttk

import tkintermapview
import requests


class MapApp:
    #Purpose: Manages the Tkinter window and the map widget
    def __init__(self, width=1200, height=1000, title="Map Viewer"):
        #Initialize the Tkinter window and map widget
        self.root = tk.Tk()
        self.root.geometry(f"{width}x{height}")
        self.root.title(title)

        # Create map widget
        self.map_widget = tkintermapview.TkinterMapView(self.root, width=width, height=height, corner_radius=0)
        self.map_widget.pack()

    def set_initial_position(self, latitude, longitude, zoom=0):
        #Set the map's initial position and zoom level
        self.map_widget.set_position(latitude, longitude, zoom)

    def add_marker(self, latitude, longitude, label):
        #Add a marker to the map at the specified coordinates with a label
        self.map_widget.set_marker(latitude, longitude, label)

    def add_path(self, path, color):
        #Draw a line path on the map between a sequence of points
        self.map_widget.set_path(path, color=color)

    def run(self):
        #Start the Tkinter main loop
        self.root.mainloop()


class RouteData:
    #Purpose: Handles fetching and parsing route data from a URL
    def __init__(self, url):
        #Fetch and store route data from a given URL
        self.data = self.fetch_data(url)

    @staticmethod
    def fetch_data(url):
        #Request data from a URL and return as plain text
        response = requests.get(url)
        return response.text

    def parse_data(self):
        #Parse the CSV route data into a list of (lat, lon, temperature, humidity) tuples
        lines = self.data.strip().split('\n')
        coordinates = []
        humidity_data = []

        for line in lines:
            values = line.split(',')
            if len(values) == 5:
                _, latitude, longitude, temperature, humidity = values
                if (latitude, longitude, temperature) in coordinates:
                    continue
                coordinates.append((float(latitude), float(longitude), float(temperature)))
                humidity_data.append((float(latitude), float(longitude), int(humidity)))

        return coordinates, humidity_data


class RouteVisualizer:
    #Purpose: Responsible for visualizing the route on the map using the provided coordinates and humidity data
    def __init__(self, map_app, coordinates, humidity_data):
        #Initialize with a MapApp instance and route data
        self.map_app = map_app
        self.coordinates = coordinates
        self.humidity_data = humidity_data

    @staticmethod
    def get_color(temperature):
        #Determine line color based on temperature
        if temperature < 0:
            return 'lightcyan'
        elif 0 <= temperature < 10:
            return 'cyan'
        elif 10 <= temperature < 15:
            return 'mediumspringgreen'
        elif 15 <= temperature < 20:
            return 'springgreen'
        elif 20 <= temperature < 25:
            return 'lime'
        elif 25 <= temperature < 30:
            return 'limegreen'
        elif 30 <= temperature < 35:
            return 'green'
        elif 35 <= temperature < 40:
            return 'tomato'
        elif 40 <= temperature < 45:
            return 'orangered'
        else:
            return 'red'

    def add_markers(self):
        #Add starting, destination, and humidity markers
        if self.coordinates:
            start_lat, start_lon, _ = self.coordinates[0]
            end_lat, end_lon, _ = self.coordinates[-1]

            # Starting and destination markers
            self.map_app.add_marker(start_lat, start_lon, f'Starting point! Humidity: {self.humidity_data[0][2]}%')
            self.map_app.add_marker(end_lat, end_lon, f'Destination! Humidity: {self.humidity_data[-1][2]}%')
            self.map_app.set_initial_position(start_lat, start_lon, zoom=10)

            # Humidity markers
            for i in range(len(self.humidity_data) - 1):
                if self.humidity_data[i][2] != self.humidity_data[i + 1][2]:
                    lat, lon, humidity = self.humidity_data[i + 1]
                    self.map_app.add_marker(lat, lon, f'Humidity: {humidity}%')

    def draw_paths(self):
        #Draw paths between coordinates with color indicating temperature
        for i in range(1, len(self.coordinates)):
            lat1, lon1, temp1 = self.coordinates[i - 1]
            lat2, lon2, temp2 = self.coordinates[i]
            color = self.get_color(temp1)
            self.map_app.add_path([(lat1, lon1), (lat2, lon2)], color=color)

    def visualize(self):
        #Run visualization by adding markers and drawing paths
        self.add_markers()
        self.draw_paths()


if __name__ == "__main__":
    # Initialize Map Application
    app = MapApp()


    # Fetch route data
    route_url = 'https://fl-17-240.zhdk.cloud.switch.ch/containers/grp2/routes/demo1?start=0&end=-1&format=csv'
    route_data = RouteData(route_url)
    coordinates, humidity_data = route_data.parse_data()

    # Visualize route
    visualizer = RouteVisualizer(app, coordinates, humidity_data)
    visualizer.visualize()

    # Run the Tkinter app
    app.run()
