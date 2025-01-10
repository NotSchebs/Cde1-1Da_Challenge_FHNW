import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


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