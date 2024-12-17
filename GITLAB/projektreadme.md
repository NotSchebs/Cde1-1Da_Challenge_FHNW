 # Container Simulator
Code um eine geojson datei auf den Server zu laden:
![img_1.png](img_1.png)

Erklärung der Klassen:
1. MapApp Klasse
Zweck: Verwaltet das Tkinter-Fenster und das Karten-Widget.

Initialisierung (__init__):

Erstellt das Hauptfenster von Tkinter (Titel, Größe).
Erstellt das Karten-Widget (tkintermapview.TkinterMapView) und fügt es in das Fenster ein.
Methoden:

set_initial_position(latitude, longitude, zoom): Legt die anfängliche Ansicht der Karte auf die angegebenen Koordinaten und den Zoom-Level fest.
add_marker(latitude, longitude, label): Fügt einen Marker an den angegebenen Koordinaten mit einem Label (z. B. zur Anzeige der Luftfeuchtigkeit) zur Karte hinzu.
add_path(path, color): Zeichnet einen Pfad zwischen angegebenen Punkten in der festgelegten Farbe auf die Karte.
run(): Startet die Haupt-Ereignisschleife von Tkinter und ermöglicht die Ausführung und Interaktion der Anwendung.
2. RouteData Klasse
Zweck: Holt und analysiert die Routendaten von einer URL.

Initialisierung (__init__):

Nimmt eine URL als Argument und ruft mit der Methode fetch_data die Daten von dieser URL ab.
Methoden:

fetch_data(url): Eine statische Methode, die eine GET-Anfrage an die angegebene URL sendet und den Antworttext zurückgibt.
parse_data(): Verarbeitet die abgerufenen CSV-Daten:
Teilt die Daten in Zeilen auf.
Extrahiert relevante Werte (Breitengrad, Längengrad, Temperatur, Luftfeuchtigkeit) aus jeder Zeile.
Gibt zwei Listen zurück: eine für die Koordinaten (mit Temperatur) und eine für die Luftfeuchtigkeitsdaten.
3. RouteVisualizer Klasse
Zweck: Verantwortlich für die Darstellung der Route auf der Karte mithilfe der bereitgestellten Koordinaten und Luftfeuchtigkeitsdaten.

Initialisierung (__init__):

Nimmt eine Instanz von MapApp und die analysierten Routendaten (Koordinaten und Luftfeuchtigkeit) entgegen.
Methoden:

get_color(temperature): Bestimmt und gibt eine Farbe basierend auf der Temperatur zurück. Diese Farbe wird verwendet, um die Temperaturunterschiede entlang des Pfads darzustellen.
add_markers():
Fügt Marker für den Startpunkt, das Ziel und Punkte mit unterschiedlicher Luftfeuchtigkeit zur Karte hinzu.
Legt die anfängliche Position der Karte auf den Startpunkt fest.
draw_paths(): Durchläuft die Liste der Koordinaten und zeichnet Pfade zwischen diesen. Jedes Pfadsegment wird je nach Temperatur an seinem Startpunkt eingefärbt.
visualize(): Führt den Visualisierungsprozess durch, indem es add_markers() und draw_paths() aufruft, um die Daten auf der Karte darzustellen.
Hauptausführungsblock
Der Hauptteil des Codes außerhalb der Klassen:
Initialisiert eine Instanz von MapApp.
Erstellt eine Instanz von RouteData, ruft die Routendaten von der angegebenen URL ab und analysiert diese in Koordinaten- und Luftfeuchtigkeitsdaten.
Initialisiert eine Instanz von RouteVisualizer, übergibt die Map-App und die analysierten Daten.
Ruft die visualize()-Methode auf, um Marker zu platzieren und Pfade auf der Karte zu zeichnen.
Startet schließlich die Tkinter-Anwendung mit app.run().
Zusammenfassung
Zusammengefasst organisiert diese objektorientierte Struktur den Code in klare Komponenten, die jeweils eine bestimmte Funktion erfüllen:

MapApp für die Verwaltung der Kartendarstellung,
RouteData für das Abrufen und Analysieren der Daten,
RouteVisualizer für die visuelle Darstellung auf der Karte.