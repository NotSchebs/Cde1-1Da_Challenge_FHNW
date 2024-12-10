
import time
import paho.mqtt.client as mqtt
import csv
import requests  # Für das Abrufen der Datei von einer URL

# MQTT Broker Konfiguration
BROKER_URL = "fl-17-240.zhdk.cloud.switch.ch"
BROKER_PORT = 9001  # WebSocket-Port
TOPIC = "migros/grp2/demo1"  # Das zu abonnierende Topic

# Funktion, um die CSV-Datei von einer URL zu laden
def load_csv_from_url(url):
    response = requests.get(url)
    response.raise_for_status()  # Falls die Anfrage fehlschlägt, wird eine Ausnahme ausgelöst
    return response.text  # Gibt den Inhalt der CSV als Text zurück

# Callback-Funktion für den Verbindungsaufbau
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Verbindung erfolgreich!")
    else:
        print(f"Verbindung fehlgeschlagen mit Fehlercode {rc}")

# Funktion, um die CSV-Datei Zeile für Zeile zu publizieren
def publish_csv_lines(client, csv_content):
    # CSV-Inhalt im Textformat lesen
    csv_reader = csv.reader(csv_content.splitlines())
    for row in csv_reader:
        # Jede Zeile wird als Nachricht veröffentlicht
        payload = ', '.join(row)  # Konvertiere die Zeile in einen String
        client.publish(TOPIC, payload)
        print(f"Gesendet: {payload} an {TOPIC}")
        time.sleep(0.1)  # Verzögerung von 0,1 Sekunden

# MQTT-Client initialisieren
client = mqtt.Client(transport="websockets")  # WebSocket als Transportprotokoll
client.on_connect = on_connect  # Callback für Verbindungsaufbau

try:
    # Verbindung zum MQTT Broker herstellen
    print("Verbindung wird aufgebaut...")
    client.connect(BROKER_URL, BROKER_PORT, 60)
    client.loop_start()  # Startet den MQTT-Loop, um Nachrichten zu empfangen

    # CSV-Datei von der URL laden
    print("Lade CSV-Datei...")
    csv_content = load_csv_from_url("https://fl-17-240.zhdk.cloud.switch.ch/containers/grp2/routes/demo1?start=0&end=-1&format=csv")  #https://fl-17-240.zhdk.cloud.switch.ch/containers/grp2/routes/demo1/info
    print("CSV-Datei erfolgreich geladen.")

    # Jede Zeile der CSV-Datei über MQTT veröffentlichen
    print("Starte Ausgabe der CSV-Zeilen...")
    publish_csv_lines(client, csv_content)

    # MQTT-Loop stoppen und Verbindung trennen
    client.loop_stop()  # Stoppt den Loop
    client.disconnect()  # Trennt die Verbindung
    print("Verbindung beendet.")

except requests.exceptions.RequestException as e:
    print(f"Fehler beim Abrufen der Datei: {e}")
except Exception as e:
    print(f"Fehler: {e}")
