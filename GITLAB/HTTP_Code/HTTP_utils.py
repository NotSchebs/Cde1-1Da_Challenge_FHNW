import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from HTTP_Route_visualizer import RouteVisualizer

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

def plot_popup(tem, lf):
    """Display the temperature and humidity plot in a Tkinter popup."""
    # Create a popup window
    popup3 = tk.Toplevel()
    popup3.title("Temperature and Humidity Plot")
    popup3.geometry("800x600")  # Adjust the size of the popup
    # Implementieren der Daten (Raumtemperatur(temp)) und (Luftfeuchtigkeit(LF))
    #Für die X achse wird die Anzahl werte von der Raumtemperatur genommen da sie gleich viele werte hat wie die Luftfeuchtigkeit
    x = list(range(len(tem)))
    y1 = tem
    y2 = lf
    # Neues Figure- und Axes-Objekt erstellen
    fig, ax1 = plt.subplots(figsize=(10, 10))
    # Zweites Axes erstellen, das dieselbe x-Achse teilt
    ax2 = ax1.twinx()
    # Daten auf jedem Axes plotten
    ax1.plot(x, y1, 'b-', label='Temperatur')
    ax2.plot(x, y2, 'r-', label='Luftfeuchtigkeit')
    # Y-Achsen-Beschriftungen festlegen
    ax1.set_ylabel('Temperatur', color='b')
    ax2.set_ylabel('Luftfeuchtigkeit', color='r')
    # X-Achsen-Beschriftung hinzufügen
    ax1.set_xlabel('Zurückgelegte Strecke in %', color='g')
    #X-Achsen-Beschriftungen in Prozent festlegen
    ax1.set_xlim(0, len(x) - 1)
    ax1.xaxis.set_major_locator(ticker.MultipleLocator((len(x)-1) / 10))
    ax1.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'{int(round(x / (len(tem) - 1) * 100))}%'))
    # Embed the Matplotlib figure into the Tkinter popup
    canvas = FigureCanvasTkAgg(fig, master=popup3)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    # Add a close button
    close_button = ttk.Button(popup3, text="Close", command=popup3.destroy)
    close_button.pack(pady=10)
    # popup3.mainloop()
