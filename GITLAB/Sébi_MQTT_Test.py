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
        coord = []
        hum_dat = []
        tem = []
        lf = []

        for line in lines:
            values = line.split(',')
            if len(values) == 5:
                _, latitude, longitude, temperature, humidity = values
                if (float(latitude), float(longitude), float(temperature)) in coord:
                    continue
                coord.append((float(latitude), float(longitude), float(temperature)))
                hum_dat.append((float(latitude), float(longitude), int(humidity)))
                tem.append(float(temperature))
                lf.append(float(humidity))

        return coord, hum_dat , tem, lf

class RouteSelector:
    def __init__(self, options = None):
        """ Initialize the selector with route options.
            Default options are used if none are provided."""

        self.default_options = [
            ('Route Map demo1',
             'https://fl-17-240.zhdk.cloud.switch.ch/containers/grp2/routes/demo?start=0&end=-1&format=csv'),
            ('Route Map demo2',
             'https://fl-17-240.zhdk.cloud.switch.ch/containers/grp2/routes/demo2_extremvieledaten?start=0&end=-1&format=csv')
        ]
        # Use provided options if available; otherwise, use default options
        self.options = options if options is not None else self.default_options
        self.selected_url = None  # Store the selected URL

    @staticmethod
    def is_valid_url(url):
        """Regular expression to validate the URL"""
        url_regex = re.compile(
            r'^(?:http|https)://'  # http:// or https://
            r'(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}'  # domain
            r'(?::\d{2,5})?'  # optional port
            r'(?:[/?#]\S*)?$', re.IGNORECASE  # path/query fragment
        )
        return re.match(url_regex, url) is not None

    def submit_selection(self,var, popup, custom_entry):
        """Handle the submission of the selected option or custom URL."""
        selected_option = var.get()

        # Handle the case for the custom map URL
        if selected_option == "Custom Map URL":
            custom_url = custom_entry.get()  # Get custom URL from entry field
            if self.is_valid_url(custom_url):
                self.selected_url = custom_url
                popup.destroy()  # Close the window after selection
            else:
                messagebox.showwarning("Invalid URL", "Please enter a valid URL.")

        elif selected_option:
            label = next(label for label, url in self.options if url == selected_option)
            messagebox.showinfo("Selection", f"You selected: {label}")
            self.selected_url = selected_option
            popup.destroy()  # Close the window after selection

        else:
            messagebox.showwarning("No selection", "Please select an option.")

    def map_options(self):
        """Create the popup to Select the route or to enter a custom URL for the route"""

        popup = tk.Tk()
        popup.title("Select route!")
        #popup.geometry("600x400")

        # Variable to store the selected option
        var = tk.StringVar(value="")

        for label, url in self.options:
            tk.Radiobutton(popup, text=label, variable=var, value=url).pack(anchor="w")


        # Add a radio button for the "Other" option
        tk.Radiobutton(popup, text="Custom Map URL", variable=var, value="Custom Map URL").pack(anchor="w")

        # Entry box for custom input (always visible)
        custom_entry = tk.Entry(popup)
        custom_entry.pack(anchor="w", padx=20, pady=5)

        # Submit button to confirm selection
        submit_button = tk.Button(popup, text="Submit",
                                  command=lambda: self.submit_selection(var, popup, custom_entry))
        submit_button.pack(pady=20)

        popup.wait_window()  # Wait for the popup window to close

        return self.selected_url  # Return the selected URL after the window is closed

class RouteVisualizer:
    def __init__(self, map_app, coord, hum_data):
        """Initialize with a MapApp instance and route data"""
        self.map_app = map_app
        self.coordinates = coord
        self.humidity_data = hum_data

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

def plot_popup(tem, lf):
    """Display the temperature and humidity plot in a Tkinter popup."""
    # Create a popup window
    popup3 = tk.Toplevel()
    popup3.title("Temperature and Humidity Plot")
    popup3.geometry("800x600")  # Adjust the size of the popup

    # Implementieren der Daten (Raumtemperatur(temp)) und (Luftfeuchtigkeit(LF))
    #Für die X achse wird die Anzahl werte von der Raumtemperatur genommen da sie gleich viele werte hat wie die Luftfeuchtigkeit
    x = list(range(len(tem)))
    y1 = tem
    y2 = lf

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
    ax1.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'{int(round(x / (len(tem) - 1) * 100))}%'))

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
