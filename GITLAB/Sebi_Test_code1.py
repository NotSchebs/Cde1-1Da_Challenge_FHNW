import tkinter
import tkintermapview
# from re-import split

import requests

# create tkinter window
root_tk = tkinter.Tk()
root_tk.geometry(f"{1200}x{1000}")  # margins of the window
root_tk.title("map_view_example.py")    # title of the pop - up

# create map widget
map_widget = tkintermapview.TkinterMapView(root_tk, width=1200, height=1000, corner_radius=0) # margins of the map
map_widget.pack()   # The .pack() method controls how widgets are placed in the window
'''
side: Determines which side of the window to place the widget on ("top", "bottom", "left", "right").
fill: Specifies if the widget should expand to fill available space. Options include "x" (horizontal), "y" (vertical), or "both".
expand: If set to True, the widget expands to fill any extra space in the window.

'''
# request url for the data and response is the server response
response = requests.get('https://fl-17-240.zhdk.cloud.switch.ch/containers/grp2/routes')
#print(response.status_code)
#print(response.text)

#request url for the coordinates
coords = requests.get('https://fl-17-240.zhdk.cloud.switch.ch/containers/grp2/routes/demo?start=0&end=-1&format=csv')
#print(coords.text)
#print('--------------')

data = coords.text # assigning the coordinates df to data

# Split the data by lines
lines = data.strip().split('\n')

#Test to see how to separate all the data
'''# Process each line
for i, line in enumerate(lines):
    values = line.split(',')    #split the values 

    # Ensure we have exactly 5 values (date_time, latitude, longitude, temperature, humidity)
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
coordinates = [] # coordinate list with (latitude, longitude and temp)
humidity_coordinates = []   # coordinate list with (latitude, longitude and Humidity)
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
        humidity = int(humidity)

        # Store the coordinates
        if (latitude, longitude, temperature) in coordinates: # check if suddenly a coordinate is double(since its one-way)
            continue
        coordinates.append((latitude, longitude, temperature))
        humidity_coordinates.append((latitude, longitude, humidity))

# Start Tkinter main loop after adding all markers
if coordinates:
    first_lat, first_long, _ = coordinates[0]
    last_lat, last_long, _ = coordinates[len(coordinates)-1]

    map_widget.set_marker(first_lat, first_long, str('Starting point! Humidity: '+str(humidity_coordinates[0][2])+'%')) # Staritng point
    map_widget.set_marker(last_lat, last_long) # destination point
    map_widget.set_position(first_lat, first_long,zoom = 0) #get the map to pop up at the right position (if you don't do that it'll pop up in berlin

    # humidity markers
    for i in range(len(humidity_coordinates) - 1):
        if humidity_coordinates[i][2] != humidity_coordinates[i + 1][2]:
            map_widget.set_marker(humidity_coordinates[i+1][0], humidity_coordinates[i+1][1],str('Humidity: '+str(humidity_coordinates[i+1][2])+'%'))

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

