import time
import paho.mqtt.client as mqtt
import csv

# Benutzerdefinierte Eingabe
def get_user_input(prompt, default=None):
    user_input = input(f"{prompt} [{default}]: ").strip()
    return user_input if user_input else default

# MQTT-Konfiguration
BROKER_URL = get_user_input("Gib die MQTT-Broker-URL ein", "fl-17-240.zhdk.cloud.switch.ch")
BROKER_PORT = int(get_user_input("Gib den MQTT-Port ein", "9001"))
TOPIC = get_user_input("Gib das MQTT-Topic ein", "migros/grp2/demo1")

# Platzhalter für empfangene CSV-Daten
csv_content = []

# Callback für erfolgreiche Verbindung
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Verbindung erfolgreich!")
        # Anfrage für CSV-Daten senden
        client.publish(f"{TOPIC}/request", "SEND_CSV")
        print(f"Anfrage für CSV-Daten an {TOPIC}/request gesendet.")
    else:
        print(f"Verbindung fehlgeschlagen mit Fehlercode {rc}")

# Callback für empfangene Nachrichten
def on_message(client, userdata, msg):
    global csv_content
    if msg.topic == f"{TOPIC}/response":
        print(f"Nachricht auf {msg.topic} empfangen.")
        csv_content.append(msg.payload.decode())
    else:
        print(f"Unerwartete Nachricht auf {msg.topic}: {msg.payload.decode()}")

# CSV-Daten verarbeiten
def process_csv_data(csv_lines):
    csv_reader = csv.reader(csv_lines)
    for row in csv_reader:
        print(f"Verarbeitete Zeile: {row}")

# MQTT-Client initialisieren
client = mqtt.Client(transport="websockets")
client.on_connect = on_connect
client.on_message = on_message

try:
    # Verbindung zum MQTT-Broker herstellen
    print(f"Verbindung zu {BROKER_URL}:{BROKER_PORT} wird aufgebaut...")
    client.connect(BROKER_URL, BROKER_PORT, 60)
    client.subscribe(f"{TOPIC}/response")  # Antwort-Topic abonnieren
    client.loop_start()

    # Warten auf CSV-Daten (Timeout nach 30 Sekunden)
    print("Warte auf CSV-Daten...")
    start_time = time.time()
    while not csv_content and time.time() - start_time < 30:
        time.sleep(0.1)

    if csv_content:
        print("CSV-Daten empfangen. Verarbeitung beginnt...")
        process_csv_data(csv_content)
    else:
        print("Keine CSV-Daten empfangen.")

    # Verbindung beenden
    client.loop_stop()
    client.disconnect()
    print("Verbindung beendet.")

except Exception as e:
    print(f"Fehler: {e}")
