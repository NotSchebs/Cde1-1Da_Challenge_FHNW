import tkinter as tk
from tkinter import messagebox
import re

import tkintermapview
import requests
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from shapely.creation import empty


#fruit thing

class MapApp:
    def __init__(self, width=1200, height=1000, title="Map Viewer"):
        #Initialize the Tkinter window and map widget
        self.root = tk.Tk()
        self.root.geometry(f"{width}x{height}")
        self.root.title(title)
        self.map_widget = tkintermapview.TkinterMapView(self.root, width=width, height=height, corner_radius=0)
        self.map_widget.pack()

    def set_initial_position(self, latitude, longitude, zoom=0):
        #Set the map's initial position and zoom level
        self.map_widget.set_position(latitude, longitude, zoom)

    def add_marker(self, latitude, longitude, label):
        #Add a marker to the map at the specified coordinates with a label
        self.map_widget.set_marker(latitude, longitude, label)

    def add_path(self, path, color="black"):
        #Draw a line path on the map between a sequence of points
        self.map_widget.set_path(path, color=color)

    def run(self):
        #Start the Tkinter main loop
        self.root.mainloop()


class RouteData:
    def __init__(self, url):
        #Fetch and store route data from a given URL
        self.data = self.fetch_data(url)

    @staticmethod
    def is_valid_url(url):
        # Regular expression to validate the URL
        url_regex = re.compile(
            r'^(?:http|https)://'  # http:// or https://
            r'(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}'  # domain
            r'(?::\d{2,5})?'  # optional port
            r'(?:[/?#]\S*)?$', re.IGNORECASE  # path/query fragment
        )
        return re.match(url_regex, url) is not None

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
        temp = []
        LF = []

        for line in lines:
            values = line.split(',')
            if len(values) == 5:
                _, latitude, longitude, temperature, humidity = values
                if (latitude, longitude, temperature) in coordinates:
                    continue
                coordinates.append((float(latitude), float(longitude), float(temperature)))
                humidity_data.append((float(latitude), float(longitude), int(humidity)))
                temp.append(float(temperature))
                LF.append(float(humidity))

        return coordinates, humidity_data , temp, LF


class RouteVisualizer:
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

##### chose options

def submit_selection(var, popup2, label,custom_entry, result):
    selected_option = var.get()
    selected_label = label
    # If no predefined option is selected, use the custom entry text
    if selected_option == "Custom Map URL": #selected option
        selected_label = "Custom Map URL" #label
        selected_option = custom_entry.get()
        if not RouteData.is_valid_url(selected_option):  # Check if it's a valid URL
            messagebox.showwarning("Invalid URL", "Please enter a valid URL.")

    elif selected_option:
        messagebox.showinfo("Selection", f"You selected: {selected_label}")
        result.append(selected_option)
        popup2.destroy()  # Close the window after selection
    else:
        messagebox.showwarning("No selection", "Please select an option.")


def map_options():
    popup2 = tk.Tk()
    popup2.title("Select route!")
    popup2.geometry("600x400")

    # Variable to store the selected option
    var = tk.StringVar(value="")

    result = []

    options = [
        ('Route Map demo1', 'https://fl-17-240.zhdk.cloud.switch.ch/containers/grp2/routes/demo1?start=0&end=-1&format=csv'),
        ('Route Map demo2','https://fl-17-240.zhdk.cloud.switch.ch/containers/grp2/routes/demo2_extremvieledaten?start=0&end=-1&format=csv')
    ]
    for label, url in options:
        radio_button = tk.Radiobutton(popup2, text=label, variable=var, value=url)
        radio_button.pack(anchor="w")

    # Add a radio button for the "Other" option
    other_radio_button = tk.Radiobutton(popup2, text="Custom Map URL", variable=var, value="Custom Map URL")
    other_radio_button.pack(anchor="w")

    # Entry box for custom input (always visible)
    custom_entry = tk.Entry(popup2)
    custom_entry.pack(anchor="w", padx=20, pady=5)

    # Submit button to confirm selection
    submit_button = tk.Button(popup2, text="Submit", command=lambda: submit_selection(var, popup2, label,custom_entry, result))
    submit_button.pack(pady=20)

    popup2.wait_window()  # Wait for the popup window to close

    return result[0] if result else None # Return the value selected by the user (not the StringVar object)

# Main Execution
if __name__ == "__main__":

    # Initialize Map Application
    selected_url = map_options()
    print("Selected URL:", selected_url)

    app = MapApp()
    # Fetch route data
    route_url = selected_url
    route_data = RouteData(route_url)
    coordinates, humidity_data, temp, LF = route_data.parse_data()

    # Visualize route
    visualizer = RouteVisualizer(app, coordinates, humidity_data)
    visualizer.visualize()

    # Implementieren der Daten (Raumtemperatur(temp)) und (Luftfeuchtigkeit(LF))
    #Für die X achse wird die Anzahl werte von der Raumtemperatur genommen da sie gleich viele werte hat wie die Luftfeuchtigkeit
    x = list(range(len(temp)))
    y1 = temp
    y2 = LF

    # Neues Figure- und Axes-Objekt erstellen
    fig, ax1 = plt.subplots()

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

    # Abbildung anzeigen
    plt.show()

    # Run the Tkinter app
    app.run()