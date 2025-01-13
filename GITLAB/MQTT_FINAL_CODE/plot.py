import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk

class Plot:
    def __init__(self, temp_data, humidity_data):
        # Initialize with temperature and humidity data
        self.temp_data = temp_data
        self.humidity_data = humidity_data
        self.x = list(range(len(temp_data)))

        # Create a matplotlib figure and axes
        self.fig, self.ax1 = plt.subplots(figsize=(6, 4))
        self.ax2 = self.ax1.twinx()

        self.canvas = None

    def initialize_plot(self, parent):
        # Create a popup window for the plot
        self.popup = tk.Toplevel(parent)
        self.popup.title("Temperature and Humidity Plot")

        # Plot temperature and humidity data
        self.line_temp, = self.ax1.plot(self.x, self.temp_data, 'b-', label='Temperature')
        self.line_humidity, = self.ax2.plot(self.x, self.humidity_data, 'r-', label='Humidity')

        # Set axis labels
        self.ax1.set_xlabel("Steps")
        self.ax1.set_ylabel("Temperature (°C)", color='b')
        self.ax2.set_ylabel("Humidity (%)", color='r')

        # Embed the plot in the popup
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.popup)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        self.canvas.draw()

    def update_plot(self, new_temp, new_humidity):
        # Add new data points
        self.temp_data.extend(new_temp)
        self.humidity_data.extend(new_humidity)
        self.x = list(range(len(self.temp_data)))

        # Update plot data
        self.line_temp.set_data(self.x, self.temp_data)
        self.line_humidity.set_data(self.x, self.humidity_data)

        # Adjust axis limits
        self.ax1.relim()
        self.ax1.autoscale_view()
        self.ax2.relim()
        self.ax2.autoscale_view()

        # Redraw the plot
        self.canvas.draw()
