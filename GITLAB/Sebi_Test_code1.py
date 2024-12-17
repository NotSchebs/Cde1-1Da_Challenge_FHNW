import time
import tkinter as tk
from tkinter import messagebox
import re
import threading
import random
import tkintermapview
import requests
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class MapApp:
    def __init__(self, width=1200, height=1000, title="Map Viewer"):
        """Initialize the Tkinter window and map widget"""
        self.root = tk.Tk()
        self.root.geometry(f"{width}x{height}")
        self.root.title(title)
        self.map_widget = tkintermapview.TkinterMapView(self.root, width=width, height=height, corner_radius=0)
        self.map_widget.pack()

    def set_initial_position(self, latitude, longitude, zoom=0):
        """Set the map's initial position and zoom level"""
        self.map_widget.set_position(latitude, longitude, zoom)

    def add_marker(self, latitude, longitude, label):
        """dd a marker to the map at the specified coordinates with a label"""
        self.map_widget.set_marker(latitude, longitude, label)

    def add_path(self, path, color="black"):
        """Draw a line path on the map between a sequence of points"""
        self.map_widget.set_path(path, color=color)

    def run(self):
        """Start the Tkinter main loop"""
        self.root.mainloop()

class RealTimeDataSimulator:
    def __init__(self, data, delay=0.05):
        """
        Simulate real-time data streaming.
        :param data: Full list of route data to simulate incoming data.
        :param delay: Delay between each data chunk (in seconds).
        """
        self.data = data
        self.delay = delay

    def datastream(self):
        """Generator that simulates data being sent in chunks."""
        for i in range(1, len(self.data) + 1):
            yield self.data[:i]  # Yield a subset of the data
            time.sleep(self.delay)  # Simulate delay for real-time effect

class RouteData:
    def __init__(self, url):
        """Fetch and store route data from a given URL"""
        self.url = url
        self.data = self.fetch_data(url)

    @staticmethod
    def fetch_data(url):
        """Request data from a URL and return as plain text"""
        response = requests.get(url, verify=False) # to ignore insecure website
        return response.text

    def parse_data(self):
        """Parse the CSV route data into a list of (lat, lon, temperature, humidity) tuples"""
        lines = self.data.strip().split("\n")
        parsed_data = []

        for line in lines:
            values = line.split(',')
            if len(values) >= 5:  # Ensure there are at least 5 elements
                try:
                    lat = float(values[1])
                    lon = float(values[2])
                    temp = float(values[3])
                    humidity = int(values[4])
                    parsed_data.append((lat, lon, temp, humidity))
                except ValueError:
                    # Skip invalid lines that cannot be converted properly
                    print(f"Skipping invalid line: {line}")
            else:
                print(f"Skipping incomplete line: {line}")

        return parsed_data

class RouteSelector:
    def __init__(self, options=None):
        """Initialize the selector with route options.
        Default options are used if none are provided.
        """
        self.server_option = 'https://fl-17-240.zhdk.cloud.switch.ch/'  # Default server URL
        self.default_options = [
            ('Route Map demo1',
             self.server_option + 'containers/grp2/routes/demo?start=0&end=-1&format=csv'),
            ('Route Map demo2',
             self.server_option + 'containers/grp2/routes/demo2_extremvieledaten?start=0&end=-1&format=csv')
        ]
        # Use provided options if available; otherwise, use default options
        self.options = options if options is not None else self.default_options
        self.selected_server = self.server_option
        self.selected_url = None  # Store the selected route URL

    @staticmethod
    def is_valid_url(url):
        """Validate the URL using a regular expression."""
        url_regex = re.compile(
            r'^(?:http|https)://'  # http:// or https://
            r'(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}'  # domain
            r'(?::\d{2,5})?'  # optional port
            r'(?:[/?#]\S*)?$', re.IGNORECASE  # path/query fragment
        )
        return re.match(url_regex, url) is not None

    def submit_server_selection(self, var, server_popup, custom_entry):
        """Handle the submission of the selected server option or custom server URL."""
        selected_option = var.get()

        if selected_option == "Custom Server URL":
            custom_url = custom_entry.get().strip()
            if self.is_valid_url(custom_url):
                self.selected_server = custom_url
                server_popup.destroy()
            else:
                messagebox.showwarning("Invalid URL", "Please enter a valid server URL.")
        elif selected_option:
            self.selected_server = selected_option
            server_popup.destroy()
        else:
            messagebox.showwarning("No selection", "Please select a server or enter a custom URL.")

    def select_server(self):
        """Create the popup to select or input the server URL."""
        server_popup = tk.Tk()
        server_popup.title("Select Server")

        # Variable to store the selected option
        var = tk.StringVar(value="")

        # Radio buttons for default server and custom server
        tk.Radiobutton(
            server_popup,
            text=f"Original Server: {self.server_option}",
            variable=var,
            value=self.server_option
        ).pack(anchor="w")

        tk.Radiobutton(
            server_popup,
            text="Custom Server URL",
            variable=var,
            value="Custom Server URL"
        ).pack(anchor="w")

        # Entry box for custom server input
        custom_entry = tk.Entry(server_popup)
        custom_entry.pack(anchor="w", padx=20, pady=5)

        # Submit button to confirm server selection
        submit_button = tk.Button(
            server_popup,
            text="Submit",
            command=lambda: self.submit_server_selection(var, server_popup, custom_entry)
        )
        submit_button.pack(pady=20)

        server_popup.wait_window()

    def submit_route_selection(self, var, route_popup, custom_entry):
        """Handle the submission of the selected route option or custom route URL."""
        selected_option = var.get()

        if selected_option == "Custom Map URL":
            custom_url = custom_entry.get().strip()
            if self.is_valid_url(custom_url):
                self.selected_url = custom_url
                route_popup.destroy()
            else:
                messagebox.showwarning("Invalid URL", "Please enter a valid route URL.")
        elif selected_option:
            self.selected_url = selected_option
            route_popup.destroy()
        else:
            messagebox.showwarning("No selection", "Please select a route or enter a custom URL.")

    def select_route(self):
        """Create the popup to select a route or enter a custom route URL."""
        route_popup = tk.Tk()
        route_popup.title("Select Route")

        # Variable to store the selected option
        var = tk.StringVar(value="")

        # Radio buttons for route options
        for label, url in self.options:
            tk.Radiobutton(route_popup, text=label, variable=var, value=url).pack(anchor="w")

        # Radio button for custom route URL
        tk.Radiobutton(route_popup, text="Custom Map URL", variable=var, value="Custom Map URL").pack(anchor="w")

        # Entry box for custom route input
        custom_entry = tk.Entry(route_popup)
        custom_entry.pack(anchor="w", padx=20, pady=5)

        # Submit button to confirm route selection
        submit_button = tk.Button(
            route_popup,
            text="Submit",
            command=lambda: self.submit_route_selection(var, route_popup, custom_entry)
        )
        submit_button.pack(pady=20)

        route_popup.wait_window()

    def map_options(self):
        """Main method to run server selection and then route selection."""
        # First, select the server
        self.select_server()

        if not self.selected_server:
            messagebox.showerror("Error", "Server selection failed.")
            return None

        # Update route URLs with the selected server
        self.options = [
            (label, url.replace(self.server_option, self.selected_server))
            for label, url in self.default_options
        ]

        # Then, select the route
        self.select_route()

        if not self.selected_url:
            messagebox.showerror("Error", "Route selection failed.")
            return None

        return self.selected_url

class RouteVisualizer:
    def __init__(self, map_app, coordinates, humidity_data):
        """Initialize with a MapApp instance and route data"""
        self.map_app = map_app
        self.coordinates = coordinates
        self.humidity_data = humidity_data
        self.markers = []  # Keep track of markers
        self.markers_track = []  # Track visited points
        self.hum_record = []  # Keep track of humidity changes
        self.visited_points = set()  # Set to track unique coordinates
        self.start_point_added = False  # Flag to track if the start point is added

    def update_markers_and_paths(self, new_coordinates, humidity_data):
        """Update the map with new coordinates dynamically."""

        for i, (lat, lon, temp, humidity) in enumerate(new_coordinates):
            current_point = (lat, lon)

            # Skip the point if it has been visited already (don't reprocess it)
            if current_point in self.visited_points:
                continue

            # Mark the point as visited
            self.visited_points.add(current_point)

            # Add marker for the first point (start)
            if i == 0 and not self.start_point_added:
                self.map_app.add_marker(lat, lon, f"Start: {humidity}%")
                self.map_app.set_initial_position(lat, lon, zoom=10)  # Set map view on start point
                self.markers_track.append(current_point)
                self.hum_record.append(humidity)
                self.start_point_added = True  # Mark the start point added

            # Add a marker when humidity changes (only if it changed from the previous)
            elif i > 0 and humidity != self.hum_record[-1]:
                self.map_app.add_marker(lat, lon, f"Humidity: {humidity}%")
                self.map_app.set_initial_position(lat, lon, zoom=10)
                self.hum_record.append(humidity)

            # Draw path between consecutive coordinates
            if i > 0:
                prev_lat, prev_lon, _, _ = new_coordinates[i - 1]
                self.map_app.add_path([(prev_lat, prev_lon), (lat, lon)], color=self.get_color(temp))

            # Always track this point for the path history
            self.markers_track.append(current_point)

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
        self.ax1.set_ylabel("Temperature", color='b')
        self.ax2.set_ylabel("Humidity", color='r')

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.popup)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        self.canvas.draw()

    def update_plot(self, new_temp, new_humidity):
        """Update the plot with new data."""
        self.temp_data = new_temp
        self.humidity_data = new_humidity
        self.x = list(range(len(new_temp)))

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

# Simulate Real-Time Updates
def simulate_real_time_updates(map_app, visualizer, plot_updater, full_data):
    """Simulate incoming data and update the map and plot."""
    simulator = RealTimeDataSimulator(full_data)
    for new_data in simulator.datastream():
        coordinates = [(lat, lon, temp, humidity) for lat, lon, temp, humidity in new_data]
        humidity_data = [humidity for _, _, _, humidity in new_data]
        temp_data = [temp for _, _, temp, _ in new_data]

        visualizer.update_markers_and_paths(coordinates, humidity_data)
        plot_updater.update_plot(temp_data, humidity_data)


# Main Execution
if __name__ == "__main__":

    #create Map selection popup
    selector = RouteSelector()
    selected_url = selector.map_options()
    print("Selected URL:", selected_url)

    # Fetch data
    route_data = RouteData(selected_url)
    full_data = route_data.parse_data()

    # Initialize Map Application
    app = MapApp()

    # Visualize route
    visualizer = RouteVisualizer(app, [], [])
    plot_updater = Plot([], [])

    # Abbildung anzeigen
    # Initialize the plot popup
    plot_updater.initialize_plot(app.root)
    erstelle_legende()

    # Start real-time simulation on a new thread
    threading.Thread(target=simulate_real_time_updates,
                     args=(app, visualizer, plot_updater, full_data),
                     daemon=True).start()

    # Run the app
    app.run()