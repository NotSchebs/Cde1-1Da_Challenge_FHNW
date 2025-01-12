
# Projekt: Routen-Karten-Anwendung

## Übersicht
Dieses Projekt ist eine umfassende Python-Anwendung zur Erstellung und Visualisierung von Routen-Karten, mit der Benutzer:

- Optimale Routen auswählen können.
- Routen-Visualisierungen generieren können.
- Profile scannen und routenbezogene Daten analysieren können.
- MQTT-Daten in Echtzeit für dynamische Updates integrieren können.

## Ordnerstruktur und Dateien

### Root-Dateien
- **`main.py`**: Der Einstiegspunkt der Anwendung. Initialisiert das Programm und verbindet alle Module.
- **`legend_creator.py`**: Generiert Legenden für Routen-Karten, um Klarheit und bessere Visualisierungen zu gewährleisten.
- **`map_app.py`**: Verantwortlich für kartenbezogene Funktionen, einschließlich Laden und Integration von Routen.
- **`plot.py`**: Visualisiert Daten und erstellt Graphen zu Routen.
- **`profile_scan.py`**: Scannt und analysiert Profile, die sich auf Routen beziehen, und liefert detaillierte Einblicke in die Daten.
- **`route_data.py`**: Verarbeitet und verwaltet Daten zu Routen.
- **`route_selector.py`**: Ermöglicht die Auswahl spezifischer Routen basierend auf vordefinierten Kriterien.
- **`route_visualizer.py`**: Erstellt interaktive und benutzerfreundliche Visualisierungen für Routen.
- **`MQTT_Hartcodiert.py`**: Handhabt die MQTT-Integration, um in Echtzeit Daten zu empfangen und Updates zu verarbeiten.
- **`Venvstart.py`**: Ein Hilfsskript zur Initialisierung und Verwaltung der virtuellen Umgebung.
- **`requirements.txt`**: Listet die benötigten Python-Bibliotheken für das Projekt.
- **`.gitignore`**: Definiert Dateien und Verzeichnisse, die von der Versionskontrolle ignoriert werden sollen.
- **`.name`**: Projektname für die lokale Entwicklung.

### HTTP Simulations-Interaktiver Code (`HTTP_Sim_Interactive_Code`)
Dieser Ordner enthält simulationsspezifische Skripte für interaktive HTTP-basierte Simulationen.

- **`Sim_Main.py`**: Hauptskript für interaktive HTTP-Simulationen.
- **`Sim_map_app.py`**: Simulierte Kartenanwendung für Tests.
- **`Sim_plot.py`**: Modul zur Visualisierung von Temperatur- und Feuchtigkeitsänderungen.
- **`Sim_real_time.py`**: Behandelt Echtzeitsimulationen und Updates.
- **`Sim_route_data.py`**: Verarbeitet simulationsbezogene Routendaten.
- **`Sim_route_selector.py`**: Modul zur Auswahl von Routen basierend auf Kriterien.
- **`Sim_route_visualizer.py`**: Visualisiert dynamisch Routen in Simulationen.
- **`Sim_util.py`**: Hilfsfunktionen für simulationsspezifische Aufgaben.

### HTTP Simulations-Interaktiver Code mit Text (`HTTP_Sim_Interactive_mit_txt_Code`)
Dieser Ordner bietet alternative Implementierungen für HTTP-Simulationen unter Verwendung textbasierter Konfigurationen.

- **`routes.csv`**: Enthält Routendaten für Simulationen.
- **`Sim_Main.py`**: Hauptskript für Simulationen mit textbasierten Konfigurationen.
- **`Sim_map_app.py`**: Kartenmodul für Simulationen.
- **`Sim_plot.py`**: Plot-Modul für Visualisierungen.
- **`Sim_real_time.py`**: Echtzeit-Simulationsmodul.
- **`Sim_route_data.py`**: Datenmodul für Routen.
- **`Sim_route_selector.py`**: Modul zur Auswahl von Routen basierend auf Kriterien.
- **`Sim_route_visualizer.py`**: Visualisiert Routen in Simulationen.
- **`Sim_util.py`**: Hilfsfunktionen für Simulationen.
- **`Variable_Server_URL.txt`**: Enthält Server-URLs für Simulationen.

### HTTP Code (`HTTP_Code`)
Dieser Ordner enthält Skripte, die speziell für HTTP-basierte Funktionen der Anwendung entwickelt wurden.

- **`HTTP_Main.py`**: Hauptskript zur Verwaltung von HTTP-Operationen.
- **`HTTP_MapApp.py`**: Kartenmodul für HTTP-Szenarien.
- **`HTTP_Route_selector.py`**: Modul zur Auswahl von Routen in HTTP-Anwendungen.
- **`HTTP_Route_visualizer.py`**: Visualisiert dynamisch Routen in HTTP-Szenarien.
- **`HTTP_RouteData.py`**: Verarbeitet und speichert Routendaten für HTTP-Fälle.
- **`HTTP_utils.py`**: Hilfsfunktionen für HTTP-Operationen.

### GeoJSON-Dateien
Diese Dateien enthalten Geodaten für verschiedene Routen:

- **`demo.geojson`**: Beispielfile für grundlegende Tests.
- **`demo1.geojson`**: Detaillierte Beispieldaten für Simulationen.
- **`demo2_extremvieledaten.geojson`**: Datenintensive GeoJSON-Datei.
- **`demo3.geojson`**: Zusätzliche Beispieldaten.
- **`horw-engelberg.geojson`**: Route von Horw nach Engelberg.
- **`horw-luzern.geojson`**: Route von Horw nach Luzern.
- **`kriens-horw.geojson`**: Route von Kriens nach Horw.
- **`luzern-horw.geojson`**: Route von Luzern nach Horw.
- **`olten-brugg.geojson`**: Route von Olten nach Brugg.

### IntelliJ IDEA Projektdateien
Diese Dateien unterstützen die Projektverwaltung in IntelliJ IDEA:

- **`profiles_settings.xml`**: Einstellungen für Inspektionen des Projekts.
- **`misc.xml`**: Enthält SDK- und Projektinformationen.
- **`modules.xml`**: Verwaltung der Projektmodule.
- **`vcs.xml`**: Versionskontrolleinstellungen (z. B. Git).
- **`GITLAB.iml`**: Moduldatei für IntelliJ IDEA.

### Weitere Dateien und Logs
- **`simulator.py`**: Simuliert Routen- und MQTT-Daten.
- **`simulator.log`**: Log-Dateien zur Überwachung und Fehlerbehebung.
- **`config-switch.ini`**: Konfigurationsdatei für HTTP-Simulationen.
- **`configuration.ini`**: Konfigurationsdatei für MQTT-basierte Simulationen.
- **`profile.py`**: Simuliert Temperatur- und Feuchtigkeitsprofile.
- **`mqtt.py`**: Handhabt die MQTT-Kommunikation.
- **`http.py`**: Verarbeitet HTTP-Kommunikation.

## Installation und Einrichtung
1. Klone das Repository auf deinen lokalen Computer.
2. Navigiere in das Projektverzeichnis.
3. Führe die folgenden Befehle aus, um eine virtuelle Umgebung einzurichten und Abhängigkeiten zu installieren:
   ```bash
   python Venvstart.py
   source venv/bin/activate  # Für Linux/Mac
   venv\Scriptsctivate   # Für Windows
   pip install -r requirements.txt
   ```
4. Für MQTT-spezifische Funktionen stelle sicher, dass der Simulator und die Konfigurationsdateien richtig eingerichtet sind:
   - `simulator.py`
   - `config-switch.ini`

## Ausführung
1. Stelle sicher, dass die virtuelle Umgebung aktiviert ist.
2. Führe das Hauptskript aus, um die Anwendung zu starten:
   ```bash
   python main.py
   ```
3. Um MQTT-Funktionen zu nutzen, führe `MQTT_Hartcodiert.py` aus:
   ```bash
   python MQTT_Hartcodiert.py
   ```
4. Um HTTP-Simulationsskripte zu nutzen, navigiere in den jeweiligen Ordner und führe das gewünschte Skript aus, z. B.:
   ```bash
   cd HTTP_Sim_Interactive_Code
   python Sim_Main.py
   ```
5. Für HTTP-basierte Funktionen, führe Skripte aus dem Ordner `HTTP_Code` aus:
   ```bash
   cd HTTP_Code
   python HTTP_Main.py
   ```

## Funktionen
- **Routenauswahl**: Wähle die beste Route basierend auf verschiedenen Parametern.
- **Interaktive Kartenvisualisierungen**: Interagiere mit generierten Karten.
- **Profilanalyse**: Analysiere detaillierte Routenprofile.
- **Echtzeit-MQTT-Datenintegration**: Visualisiere Echtzeitdaten.
- **Anpassbare Legenden**: Füge Kartenlegenden hinzu.
- **Simulatorintegration**: Teste und debugge mit simulierten Daten.
- **Simulationsprofile**: Simuliere Temperatur- und Feuchtigkeitsänderungen.
- **Flexibles Kommunikationsmanagement**: Nutze MQTT und HTTP für robuste Datenintegration.

## Anforderungen
- Python 3.8 oder höher
- Benötigte Python-Bibliotheken (siehe `requirements.txt`)
- Zusätzliche Konfigurationen für MQTT

## Mitwirken
1. Forke das Repository.
2. Erstelle einen neuen Feature-Branch.
3. Committe deine Änderungen mit klaren Nachrichten.
4. Push den Branch und erstelle eine Pull-Anfrage.

## Lizenz
Dieses Projekt ist unter der MIT-Lizenz lizenziert. Siehe die Datei LICENSE für Details.

## Kontakt
Bei Fragen oder Unterstützung, kontaktiere uns über [E-Mail/Kommunikationskanal].

