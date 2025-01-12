import tkinter as tk
from tkinter import ttk

class LegendCreator:
    def __init__(self, parent, route_visualizer):
        self.parent = parent
        self.route_visualizer = route_visualizer

    def erstelle_legende(self):
        popup2 = tk.Toplevel(self.parent)
        popup2.wm_title("Farbverlauf Legende")

        label = ttk.Label(popup2, text="Farbverlauf für Temperaturen")
        label.pack(side="top", fill="x", pady=10)

        temperaturbereiche = [
            ("unter 0", 0), (0, 9), (10, 14), (15, 19), (20, 24),
            (25, 29), (30, 34), (35, 39), (40, 44), ("über 44", 50)
        ]

        for (start, end) in temperaturbereiche:
            frame = ttk.Frame(popup2)
            farbe = self.route_visualizer.get_color((start if isinstance(start, int) else end - 10))

            beschriftung = f"{start}°C - {end}°C" if isinstance(start, int) else f"{start}"

            farb_label = tk.Label(frame, text=beschriftung, background=farbe, width=20)
            farb_label.pack(side="left", padx=10)
            frame.pack(side="top", fill="x", pady=5)

        schliessen_button = ttk.Button(popup2, text="Schließen", command=popup2.destroy)
        schliessen_button.pack(side="top", pady=10)
