import tkinter as tk
from tkinter import ttk

class LegendCreator:
    def __init__(self, parent, route_visualizer):
        # Initialize the LegendCreator class with a parent widget and a route visualizer instance
        self.parent = parent
        self.route_visualizer = route_visualizer

    def erstelle_legende(self):
        # Create a new popup window to display the legend
        popup2 = tk.Toplevel(self.parent)
        popup2.wm_title("Farbverlauf Legende")  # Set the title of the popup window

        # Add a label at the top of the popup to describe the legend
        label = ttk.Label(popup2, text="Farbverlauf für Temperaturen")
        label.pack(side="top", fill="x", pady=10)  # Position and style the label

        # Define the temperature ranges and their corresponding colors
        temperaturbereiche = [
            ("unter 0", 0), (0, 9), (10, 14), (15, 19), (20, 24),
            (25, 29), (30, 34), (35, 39), (40, 44), ("\u00fcber 44", 50)
        ]

        # Iterate through each temperature range to create and display corresponding legend items
        for (start, end) in temperaturbereiche:
            frame = ttk.Frame(popup2)  # Create a frame for each temperature range

            # Get the color associated with the current temperature range from the route visualizer
            farbe = self.route_visualizer.get_color(
                (start if isinstance(start, int) else end - 10)  # Handle "unter 0" and "\u00fcber 44" cases
            )

            # Format the label text for the temperature range
            beschriftung = f"{start}°C - {end}°C" if isinstance(start, int) else f"{start}"

            # Create a label with the temperature range description and background color
            farb_label = tk.Label(frame, text=beschriftung, background=farbe, width=20)
            farb_label.pack(side="left", padx=10)  # Position the label inside the frame

            # Pack the frame into the popup window
            frame.pack(side="top", fill="x", pady=5)

        # Add a button to close the popup window
        schliessen_button = ttk.Button(popup2, text="Schließen", command=popup2.destroy)
        schliessen_button.pack(side="top", pady=10)  # Position the button at the bottom of the popup
