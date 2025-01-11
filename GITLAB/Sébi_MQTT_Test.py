import json
import time
import paho.mqtt.client as mqtt
import csv
import io
import sys
import os
import subprocess
import re
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import matplotlib.pyplot as plt
import requests
import tkintermapview
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import threading
from Venvstart2 import Venvstart


class MapApp:
    def __init__(self, width=1200, height=1000, title="Map Viewer"):
        """Initialize the Tkinter window and map widget"""
        self.root = tk.Tk()
        self.root.geometry(f"{width}x{height}")
        self.root.title(title)
        self.map_widget = tkintermapview.TkinterMapView(self.root, width=width, height=height, corner_radius=0)
        self.map_widget.pack()

    def set_initial_position(self, latitude, longitude, zoom=10):
        """Set the map's initial position and zoom level"""
        self.map_widget.set_position(latitude, longitude, zoom)

    def add_marker(self, latitude, longitude, label):
        """Add a marker to the map at the specified coordinates with a label"""
        self.map_widget.set_marker(latitude, longitude, label)

    def add_path(self, path, color="black"):
        """Draw a line path on the map between a sequence of points"""
        self.map_widget.set_path(path, color=color)

    def run(self):
        """Start the Tkinter main loop"""
        self.root.mainloop()

class RouteData:
    def __init__(self):
        """Fetch and store route data exclusively via MQTT."""
        self.csv_data = []  # Store CSV data dynamically from MQTT
        self.new_data_available = False  # Flag to indicate new data arrival
        self.lock = threading.Lock()  # Thread lock for thread-safe operations

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("Connected successfully!")
            client.subscribe(self.TOPIC)
            print(f"Subscribed to topic: {self.TOPIC}")
        else:
            print(f"Connection failed with error code {rc}")

    def on_message(self, client, userdata, msg):
        try:
            print(f"Message received from topic {msg.topic}")
            message = msg.payload.decode()

            # Parse JSON message
            json_data = json.loads(message)
            if "point" not in json_data:
                print("Invalid message format, missing 'point' field")
                return

            # Extract the 'point' field and split it into values
            point_data = json_data["point"].split(",")
            if len(point_data) >= 5:
                row = [
                    json_data.get("company", ""),
                    json_data.get("container", ""),
                    json_data.get("route", ""),
                    point_data[0],  # Timestamp
                    point_data[1],  # Latitude
                    point_data[2],  # Longitude
                    point_data[3],  # Temperature
                    point_data[4],  # Humidity
                ]
                with self.lock:
                    self.csv_data.append(row)  # Store CSV data dynamically
                    self.new_data_available = True  # Indicate new data arrival
                print(f"Processed row: {row}")
            else:
                print(f"Skipping invalid point data: {json_data['point']}")

        except json.JSONDecodeError as e:
            print(f"Error decoding JSON message: {e}")
        except Exception as e:
            print(f"Error processing the message: {e}")

    def receive_csv_from_mqtt(self):
        client = mqtt.Client(transport="websockets")
        client.on_connect = self.on_connect
        client.on_message = self.on_message

        # MQTT Broker Configuration
        self.BROKER_URL = "fl-17-240.zhdk.cloud.switch.ch"
        self.BROKER_PORT = 9001
        self.company = "migros"
        self.container = "grp2"
        self.route = "demo1"
        self.TOPIC = f"{self.company}/{self.container}/{self.route}"

        try:
            print("Connecting to MQTT broker...")
            client.connect(self.BROKER_URL, self.BROKER_PORT, 60)
            client.loop_forever()  # Keep the client running to continuously process messages

        except Exception as e:
            print(f"Error: {e}")

    def parse_data(self):
        """Parse the MQTT CSV route data into a list of (lat, lon, temperature, humidity) tuples."""
        parsed_data = []
        with self.lock:
            for row in self.csv_data:
                try:
                    lat = float(row[4])
                    lon = float(row[5])
                    temp = float(row[6])
                    humidity = int(row[7])
                    parsed_data.append((lat, lon, temp, humidity))
                except (ValueError, IndexError) as e:
                    print(f"Skipping invalid row: {row} | Error: {e}")

            # Clear the data after parsing to avoid reprocessing
            self.csv_data.clear()
            self.new_data_available = False  # Reset the flag after processing
        return parsed_data

    def has_new_data(self):
        """Check if new data is available."""
        with self.lock:
            return self.new_data_available

class RouteVisualizer:
    def __init__(self, map_app, coordinates, humidity_data):
        """Initialize with a MapApp instance and route data"""
        self.map_app = map_app
        self.coordinates = coordinates
        self.humidity_data = humidity_data
        self.visited_points = set()  # Set to track unique coordinates
        self.start_point_added = False  # Flag to track if the start point is added

    def update_markers_and_paths(self, new_coordinates, humidity_data):
        """Update the map with new coordinates dynamically."""
        last_point = None  # Keep track of the last drawn point
        for i, (lat, lon, temp, humidity) in enumerate(new_coordinates):
            current_point = (lat, lon)

            # Skip the point if it has been visited already
            if current_point in self.visited_points:
                continue

            self.visited_points.add(current_point)

            if i == 0 and not self.start_point_added:
                self.map_app.add_marker(lat, lon, f"Start: {humidity}%")
                self.map_app.set_initial_position(lat, lon, zoom=10)
                self.start_point_added = True

            elif humidity != self.humidity_data[-1] if self.humidity_data else True:
                self.map_app.add_marker(lat, lon, f"Humidity: {humidity}%")

            # Draw path between the last point and the current one
            if last_point:
                self.map_app.add_path([last_point, current_point], color=self.get_color(temp))

            last_point = current_point
            self.humidity_data.append(humidity)

    @staticmethod
    def get_color(temperature):
        """Determine line color based on temperature"""
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

class Plot:
    def __init__(self, temp_data, humidity_data):
        self.temp_data = temp_data
        self.humidity_data = humidity_data
        self.x = list(range(len(temp_data)))
        self.fig, self.ax1 = plt.subplots(figsize=(6, 4))
        self.ax2 = self.ax1.twinx()
        self.canvas = None

    def initialize_plot(self, parent):
        """Create the popup window for the plot."""
        self.popup = tk.Toplevel(parent)
        self.popup.title("Temperature and Humidity Plot")

        self.line_temp, = self.ax1.plot(self.x, self.temp_data, 'b-', label='Temperature')
        self.line_humidity, = self.ax2.plot(self.x, self.humidity_data, 'r-', label='Humidity')

        self.ax1.set_xlabel("Steps")
        self.ax1.set_ylabel("Temperature (°C)", color='b')
        self.ax2.set_ylabel("Humidity (%)", color='r')

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.popup)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        self.canvas.draw()

    def update_plot(self, new_temp, new_humidity):
        """Update the plot by appending new data."""
        self.temp_data.extend(new_temp)
        self.humidity_data.extend(new_humidity)
        self.x = list(range(len(self.temp_data)))

        self.line_temp.set_data(self.x, self.temp_data)
        self.line_humidity.set_data(self.x, self.humidity_data)

        self.ax1.relim()
        self.ax1.autoscale_view()
        self.ax2.relim()
        self.ax2.autoscale_view()

        self.canvas.draw()


# Funktion, um die Legende zu erstellen
def erstelle_legende():
    popup2 = tk.Toplevel()  # Use Toplevel for non-blocking window
    popup2.wm_title("Farbverlauf Legende")

    label = ttk.Label(popup2, text="Farbverlauf für Temperaturen")
    label.pack(side="top", fill="x", pady=10)

    temperaturbereiche = [
        ("unter 0", 0), (0, 9), (10, 14), (15, 19), (20, 24),
        (25, 29), (30, 34), (35, 39), (40, 44), ("über 44", 50)
    ]

    for (start, end) in temperaturbereiche:
        frame = ttk.Frame(popup2)
        farbe = RouteVisualizer.get_color((start if isinstance(start, int) else end - 10))

        beschriftung = f"{start}°C - {end}°C" if isinstance(start, int) else f"{start}"

        farb_label = tk.Label(frame, text=beschriftung, background=farbe, width=20)
        farb_label.pack(side="left", padx=10)
        frame.pack(side="top", fill="x", pady=5)

    schliessen_button = ttk.Button(popup2, text="Schließen", command=popup2.destroy)
    schliessen_button.pack(side="top", pady=10)

    # popup2.mainloop()  # Start the Tkinter loop for the legend popup


# Main Execution
# Main Execution
if __name__ == "__main__":
    Venvstart()
    # Initialize Map Application
    app = MapApp()

    # Initialize Route Data and MQTT
    route_data = RouteData()

    # Function to update visualization dynamically
    def update_visualization():
        if route_data.has_new_data():
            parsed_data = route_data.parse_data()
            if parsed_data:
                # Update map visualizer
                visualizer.update_markers_and_paths(parsed_data, visualizer.humidity_data)

                # Extract temperature and humidity data
                temp_data = [point[2] for point in parsed_data]
                humidity_data = [point[3] for point in parsed_data]

                # Update the plot
                plot_updater.update_plot(temp_data, humidity_data)
                print("Plot and map updated with new data.")
        app.root.after(1000, update_visualization)


    # Function to start MQTT
    def start_mqtt():
        """Start receiving data via MQTT."""
        print("Starting MQTT to receive data...")
        route_data.receive_csv_from_mqtt()

    # Start MQTT in a separate thread
    import threading
    mqtt_thread = threading.Thread(target=start_mqtt, daemon=True)
    mqtt_thread.start()

    # Initialize Visualizer
    visualizer = RouteVisualizer(app, [], [])


    # Create and initialize plot
    plot_updater = Plot([], [])
    plot_updater.initialize_plot(app.root)

    # Display legend
    erstelle_legende()

    # Schedule the first update
    app.root.after(1000, update_visualization)

    # Run the app
    try:
        app.run()
    except KeyboardInterrupt:
        print("Application closed by user.")