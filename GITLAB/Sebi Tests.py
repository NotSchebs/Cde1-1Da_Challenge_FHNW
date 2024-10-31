'''import tkinter
import tkintermapview'''
from re import split

import requests

'''
# create tkinter window
root_tk = tkinter.Tk()
root_tk.geometry(f"{1200}x{1000}")
root_tk.title("map_view_example.py")

# create map widget
map_widget = tkintermapview.TkinterMapView(root_tk, width=1200, height=1000, corner_radius=0)
map_widget.pack(expand = True, fill = 'both')

root_tk.mainloop()'''
response = requests.get('https://fl-17-240.zhdk.cloud.switch.ch/containers/grp2/routes')
print(response.status_code)
print(response.text)

coords = requests.get('https://fl-17-240.zhdk.cloud.switch.ch/containers/grp2/routes/demo?start=0&end=-1&format=csv')
print(coords.text)
print('--------------')

data = coords.text

# Split the data by lines
lines = data.strip().split('\n')

# Process each line
for line in lines:
    # Split each line by comma
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
        print(f"Temperature: {temperature}")
        print(f"Humidity: {humidity}")
        print('--------------')
    else:
        print(f"Skipped line (unexpected format): {line}")