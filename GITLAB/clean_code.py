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
print(response.status_code)
print(response.text)

coords = requests.get('https://fl-17-240.zhdk.cloud.switch.ch/containers/grp2/routes/demo?start=0&end=-1&format=csv')
#print(coords.text)
print('--------------')

data = coords.text

# Split the data by lines
lines = data.strip().split('\n')

#Lets try to visualise all the point on the map as a line
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
        # Store the coordinates
        if (latitude, longitude) in coordinates:
            continue
        coordinates.append((latitude, longitude))


# Start Tkinter main loop after adding all markers
first_lat, first_long = coordinates[0]
last_lat, last_long = coordinates[len(coordinates)-1]
map_widget.set_marker(first_lat, first_long)
map_widget.set_marker(last_lat, last_long)
map_widget.set_position(first_lat, first_long,zoom = 0)
map_widget.set_path(coordinates) # Connect the points with a line

root_tk.mainloop()