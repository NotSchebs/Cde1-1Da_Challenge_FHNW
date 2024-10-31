#

import tkinter
import tkintermapview
import requests
from dask.dataframe.multi import required
from distributed.protocol.serialize import msgpack_decode_default
from flask import request

# create tkinter window
'''
root_tk = tkinter.Tk()
root_tk.geometry(f"{1200}x{1000}")
root_tk.title("map_view_example.py")

# create map widget
map_widget = tkintermapview.TkinterMapView(root_tk, width=1200, height=1000, corner_radius=0)
map_widget.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

root_tk.mainloop()
'''
Alle_container = requests.get( 'https://fl-17-240.zhdk.cloud.switch.ch/containers')
print(Alle_container.status_code)
print('0--------')

print(Alle_container.text)
print('1--------')
containers_controller = requests.get('https://fl-17-240.zhdk.cloud.switch.ch/containers/grp2/routes/demo?start=0&end=-1&format=csv')
print(containers_controller.text)
print('2--------')

Ale_het_de_laengsti = requests.put('https://fl-17-240.zhdk.cloud.switch.ch/containers/grp2/routes/demo')
print(Ale_het_de_laengsti.text)
print('3--------')

print(type(Ale_het_de_laengsti))  # Wenn die Antwort JSON-Daten enthält
print('4--------')

