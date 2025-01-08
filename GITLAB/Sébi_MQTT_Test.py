import time
import paho.mqtt.client as mqtt
import csv
import io
import sys
import os
import subprocess
'''
# Use the current Python interpreter
python_executable = sys.executable

# Copy the current environment variables
env = os.environ.copy()

# Ensure that the venv variables are set in the subprocess
env["VIRTUAL_ENV"] = os.environ.get("VIRTUAL_ENV", "")
env["PATH"] = os.path.dirname(python_executable) + os.pathsep + env["PATH"]

# Calling the simulator script in the background
process = subprocess.Popen(
    [
        python_executable,
        "./simulator.py",
        "./data/demo1.geojson",
        "-c",
        "./config-switch.ini",
    ],
    env=env,
)

print(f"Simulator started with PID: {process.pid}")
'''
# MQTT Broker Konfiguration
BROKER_URL = "fl-17-240.zhdk.cloud.switch.ch"  # Deine Broker-Adresse
BROKER_PORT = 9001                            # Port für WebSockets

# Dynamische Werte für das Topic
company = "migros"
container = "grp2"
route = "demo1"

TOPIC = f"{company}/{container}/{route}"  # Dynamisches Topic

# Speicherort für CSV-Daten
csv_data = []  # Liste für die CSV-Daten

# Callback für den erfolgreichen Verbindungsaufbau
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Verbindung erfolgreich!")
        client.subscribe(TOPIC)  # Topic abonnieren
        print(f"Abonniert: {TOPIC}")
    else:
        print(f"Verbindung fehlgeschlagen: Fehlercode {rc}")

# Callback für empfangene Nachrichten
def on_message(client, userdata, msg):
    global csv_data
    try:
        print(f"Nachricht empfangen: Topic: {msg.topic}")
        csv_string = msg.payload.decode()  # Nachricht dekodieren
        print("CSV-Inhalt der Nachricht:")
        print(csv_string)

        # CSV-Daten aus dem String auslesen
        csv_reader = csv.reader(io.StringIO(csv_string))
        for row in csv_reader:
            print(row)  # Zeige die Zeilen an
            csv_data.append(row)  # Speichere die CSV-Daten in der Liste

    except Exception as e:
        print(f"Fehler beim Verarbeiten der Nachricht: {e}")

# Hauptfunktion für den MQTT-Client
def receive_csv_from_mqtt():
    global csv_data
    client = mqtt.Client(transport="websockets")  # WebSocket-Transport verwenden
    client.on_connect = on_connect
    client.on_message = on_message

    try:
        print("Verbindung zum MQTT-Broker wird aufgebaut...")
        client.connect(BROKER_URL, BROKER_PORT, 60)
        client.loop_start()  # Starte die Netzwerk-Loop für MQTT

        print("Warten auf CSV-Daten (120 Sekunden)...")
        time.sleep(320)  # Wartezeit erhöhen, um Daten zu empfangen

        client.loop_stop()
        client.disconnect()
        print("Verbindung beendet.")

        # Rückgabe der gesammelten CSV-Daten
        return csv_data

    except Exception as e:
        print(f"Fehler: {e}")
        return None

# Hauptprogramm
if __name__ == "__main__":
    print("Starte MQTT-CSV-Datenempfang...")
    empfangene_daten = receive_csv_from_mqtt()

    # Zeige die empfangenen Daten an
    if empfangene_daten:
        print("Empfangene CSV-Daten:")
        for zeile in empfangene_daten:
            print(zeile)
    else:
        print("Keine CSV-Daten empfangen.")

print(csv_data)