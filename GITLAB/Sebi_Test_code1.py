import tkinter as tk
from tkinter import messagebox
import re
import tkintermapview
import requests
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

#fruit thing

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

class RouteData:
    def __init__(self, url):
        """Fetch and store route data from a given URL"""
        self.data = self.fetch_data(url)

    @staticmethod
    def fetch_data(url):
        """Request data from a URL and return as plain text"""
        response = requests.get(url, verify=False) # to ignore insecure website
        return response.text

    def parse_data(self):
        """Parse the CSV route data into a list of (lat, lon, temperature, humidity) tuples"""
        lines = self.data.strip().split('\n')
        coordinates = []
        humidity_data = []
        temp = []
        LF = []

        for line in lines:
            values = line.split(',')
            if len(values) == 5:
                _, latitude, longitude, temperature, humidity = values
                if (float(latitude), float(longitude), float(temperature)) in coordinates:
                    continue
                coordinates.append((float(latitude), float(longitude), float(temperature)))
                humidity_data.append((float(latitude), float(longitude), int(humidity)))
                temp.append(float(temperature))
                LF.append(float(humidity))

        return coordinates, humidity_data , temp, LF

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

    def add_markers(self):
        """Add starting, destination, and humidity markers"""
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
        """Draw paths between coordinates with color indicating temperature"""
        for i in range(1, len(self.coordinates)):
            lat1, lon1, temp1 = self.coordinates[i - 1]
            lat2, lon2, temp2 = self.coordinates[i]
            color = self.get_color(temp1)
            self.map_app.add_path([(lat1, lon1), (lat2, lon2)], color=color)

    def visualize(self):
        """Run visualization by adding markers and drawing paths"""
        self.add_markers()
        self.draw_paths()

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

def plot_popup(temp, LF):
    """Display the temperature and humidity plot in a Tkinter popup."""
    # Create a popup window
    popup3 = tk.Toplevel()
    popup3.title("Temperature and Humidity Plot")
    popup3.geometry("800x600")  # Adjust the size of the popup

    # Implementieren der Daten (Raumtemperatur(temp)) und (Luftfeuchtigkeit(LF))
    #Für die X achse wird die Anzahl werte von der Raumtemperatur genommen da sie gleich viele werte hat wie die Luftfeuchtigkeit
    x = list(range(len(temp)))
    y1 = temp
    y2 = LF

    # Neues Figure- und Axes-Objekt erstellen
    fig, ax1 = plt.subplots(figsize=(10, 10))

    # Zweites Axes erstellen, das dieselbe x-Achse teilt
    ax2 = ax1.twinx()

    # Daten auf jedem Axes plotten
    ax1.plot(x, y1, 'b-', label='Temperatur')
    ax2.plot(x, y2, 'r-', label='Luftfeuchtigkeit')

    # Y-Achsen-Beschriftungen festlegen
    ax1.set_ylabel('Temperatur', color='b')
    ax2.set_ylabel('Luftfeuchtigkeit', color='r')

    # X-Achsen-Beschriftung hinzufügen
    ax1.set_xlabel('Zurückgelegte Strecke in %', color='g')

    #X-Achsen-Beschriftungen in Prozent festlegen
    ax1.set_xlim(0, len(x) - 1)
    ax1.xaxis.set_major_locator(ticker.MultipleLocator((len(x)-1) / 10))
    ax1.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'{int(round(x / (len(temp) - 1) * 100))}%'))

    # Embed the Matplotlib figure into the Tkinter popup
    canvas = FigureCanvasTkAgg(fig, master=popup3)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    # Add a close button
    close_button = ttk.Button(popup3, text="Close", command=popup3.destroy)
    close_button.pack(pady=10)

    # popup3.mainloop()

# Main Execution
if __name__ == "__main__":

    #create Map selection popup
    selector = RouteSelector()
    selected_url = selector.map_options()
    print("Selected URL:", selected_url)

    # Initialize Map Application
    app = MapApp()

    # Fetch route data
    route_url = selected_url
    route_data = RouteData(route_url)
    coordinates, humidity_data, temp, LF = route_data.parse_data()

    # Visualize route
    visualizer = RouteVisualizer(app, coordinates, humidity_data)
    visualizer.visualize()

    # Abbildung anzeigen
    plot_popup(temp, LF)
    erstelle_legende()
    # Run the Tkinter app
    app.run()