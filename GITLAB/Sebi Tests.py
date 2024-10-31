import tkinter
import tkintermapview
from re import split

import requests

# create tkinter window
root_tk = tkinter.Tk()
root_tk.geometry(f"{1200}x{1000}")
root_tk.title("map_view_example.py")

# create map widget
map_widget = tkintermapview.TkinterMapView(root_tk, width=1200, height=1000, corner_radius=0)
map_widget.pack()

response = requests.get('https://fl-17-240.zhdk.cloud.switch.ch/containers/grp2/routes')
#print(response.status_code)
#print(response.text)

coords = requests.get('https://fl-17-240.zhdk.cloud.switch.ch/containers/grp2/routes/demo?start=0&end=-1&format=csv')
#print(coords.text)
#print('--------------')

data = coords.text

# Split the data by lines
lines = data.strip().split('\n')

#Test to see how to separate all the data
'''# Process each line
for i, line in enumerate(lines):
    values = line.split(',')

    # Ensure we have exactly 5 values
    if len(values) == 5:
        date_time, latitude, longitude, temperature, humidity = values

        # Convert values as needed
        latitude = float(latitude)
        longitude = float(longitude)
        temperature = float(temperature)
        humidity = int(humidity)

        # Print or use the data as needed
        print(f"Date/Time: {date_time}")
        print(f"Latitude: {latitude}")
        print(f"Longitude: {longitude}")
        print(f"Temperature: {temperature}\u00B0C")
        print(f"Humidity: {humidity}%")
        print('--------------')
    else:
        print(f"Skipped line (unexpected format): {line}")

'''

# Let's try to visualise all the point on the map as a line
coordinates = []
last_long = 0
last_lat = 0
# Process each line
for line in lines:
    values = line.split(',')

    # Ensure we have exactly 5 values
    if len(values) == 5:
        date_time, latitude, longitude, temperature, humidity = values

        # Convert values as needed
        latitude = float(latitude)
        longitude = float(longitude)
        temperature = float(temperature)

        # Store the coordinates
        if (latitude, longitude, temperature) in coordinates:
            continue
        coordinates.append((latitude, longitude, temperature))


# Start Tkinter main loop after adding all markers
if coordinates:
    first_lat, first_long, _ = coordinates[0]
    last_lat, last_long, _ = coordinates[len(coordinates)-1]
    map_widget.set_marker(first_lat, first_long)
    map_widget.set_marker(last_lat, last_long)
    map_widget.set_position(first_lat, first_long,zoom = 0)

# Function to determine color based on temperature
def get_color(temperature):
    if temperature < 0:
        return 'blue'  # Cold temperatures
    elif 0 <= temperature < 15:
        return 'lightblue'  # Cool temperatures
    elif 15 <= temperature < 25:
        return 'yellow'  # Mild temperatures
    elif 25 <= temperature < 35:
        return 'orange'  # Warm temperatures
    else:
        return 'red'  # Hot temperatures


# Draw lines between points with varying colors based on temperature
for i in range(1, len(coordinates)):
    lat1, lon1, temp1 = coordinates[i - 1]
    lat2, lon2, temp2 = coordinates[i]

    # Determine the color based on the first point of the segment
    color = get_color(temp1)

    # Draw the segment with the determined color
    map_widget.set_path([(lat1, lon1), (lat2, lon2)], color=color)

# Start Tkinter main loop
root_tk.mainloop()





