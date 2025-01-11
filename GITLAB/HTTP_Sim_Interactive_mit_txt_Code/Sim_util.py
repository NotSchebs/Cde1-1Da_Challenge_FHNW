from Sim_route_visualizer import RouteVisualizer
import tkinter as tk
from tkinter import ttk
from Sim_real_time import RealTimeDataSimulator

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

# Simulate Real-Time Updates
def simulate_real_time_updates(map_app, visualizer, plot_updater, full_data):
    """Simulate incoming data and update the map and plot."""
    simulator = RealTimeDataSimulator(full_data)
    for new_data in simulator.datastream():
        coordinates = [(lat, lon, temp, humidity) for lat, lon, temp, humidity in new_data]
        humidity_data = [humidity for _, _, _, humidity in new_data]
        temp_data = [temp for _, _, temp, _ in new_data]

        visualizer.update_markers_and_paths(coordinates, humidity_data)
        plot_updater.update_plot(temp_data, humidity_data)

def simulate_real_time_updates(app, visualizer, plot_updater, full_data, index=0):
    """Simulate incoming data and update the map and plot using Tkinter's after."""
    if index < len(full_data):
        # Fetch the next chunk of data
        new_data = full_data[:index + 1]
        coordinates = [(lat, lon, temp, humidity) for lat, lon, temp, humidity in new_data]
        humidity_data = [humidity for _, _, _, humidity in new_data]
        temp_data = [temp for _, _, temp, _ in new_data]

        # Update the map and plot
        visualizer.update_markers_and_paths(coordinates, humidity_data)
        plot_updater.update_plot(temp_data, humidity_data)

        # Schedule the next update
        app.root.after(50, simulate_real_time_updates, app, visualizer, plot_updater, full_data, index + 1)