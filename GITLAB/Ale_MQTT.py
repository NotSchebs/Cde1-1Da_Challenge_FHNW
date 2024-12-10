'''import paho.mqtt.client as mqtt
import time

# Konfiguration
BROKER_URL = "fl-17-240.zhdk.cloud.switch.ch"
BROKER_PORT = 9001  # WebSocket-Port
TRANSPORT = "websockets"  # WebSocket als Transportprotokoll
TOPIC_TEMPLATE = "{company}/{container}/{route}"  # Topic-Vorlage
UPDATE_INTERVAL = 5  # Zeitintervall zwischen Updates in Sekunden

# Transport-Details
company = "migros"  # Firma
container = "grp2"  # Container
routes = ["demo1", "demo2_extremvieledaten", "demo"]  # Routen

# Beispieldaten für Live-Updates
updates = [
    {"timestamp": "2024-12-10T10:00:00", "status": "on route", "location": "Point A"},
    {"timestamp": "2024-12-10T10:15:00", "status": "delayed", "location": "Point B"},
    {"timestamp": "2024-12-10T10:30:00", "status": "arrived", "location": "Point C"},
]

# Callback-Funktion für den Verbindungsaufbau
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Verbindung erfolgreich!")
    else:
        print(f"Verbindung fehlgeschlagen mit Fehlercode {rc}")

# MQTT-Client initialisieren
client = mqtt.Client(transport=TRANSPORT)

# Callback setzen
client.on_connect = on_connect

# Verbindung zum Broker herstellen
try:
    client.connect(BROKER_URL, BROKER_PORT, 60)
    print("Verbindung wird aufgebaut...")
    client.loop_start()  # Netzwerk-Loop starten

    # Live-Updates an alle Topics senden
    for route in routes:
        topic = TOPIC_TEMPLATE.format(company=company, container=container, route=route)
        print(f"Publizieren von Updates für Topic: {topic}")
        for update in updates:
            payload = f"{update['timestamp']}, {update['status']}, {update['location']}"
            client.publish(topic, payload)
            print(f"Gesendet: {payload} an {topic}")
            time.sleep(UPDATE_INTERVAL)  # Wartezeit zwischen Updates

    client.loop_stop()
    client.disconnect()
    print("Verbindung beendet.")
except Exception as e:
    print(f"Fehler beim Verbindungsaufbau oder Senden: {e}")

'''
import asyncio
import websockets
import paho.mqtt.client as mqtt

# WebSocket-Server
BROKER_URL = "wss://fl-17-240.zhdk.cloud.switch.ch:9001"  # Sicherstellen, dass es der WebSocket-URL ist
BROKER_PORT = 9001


async def connect_mqtt():
    # Erstelle einen MQTT-Client
    client = mqtt.Client()

    # Callback für den Verbindungsaufbau
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Verbindung erfolgreich!")
        else:
            print(f"Verbindung fehlgeschlagen mit Fehlercode {rc}")

    # Callback für eingehende Nachrichten
    def on_message(client, userdata, msg):
        print(f"Neue Nachricht empfangen von {msg.topic}")
        payload = msg.payload.decode()
        print(f"Nachricht: {payload}")

    # Callback zuweisen
    client.on_connect = on_connect
    client.on_message = on_message

    # Stelle eine Verbindung zum Broker über WebSockets her
    async with websockets.connect(BROKER_URL) as websocket:
        print("Verbunden mit WebSocket")

        # MQTT-Verbindung zu WebSocket aufbauen
        client.connect(BROKER_URL, BROKER_PORT, 60)

        # Start der Nachrichtenschleife
        client.loop_start()

        # Abonnieren des gewünschten Topics
        client.subscribe("migros/grp2/demo1")
        client.subscribe("migros/grp2/demo2_extremvieledaten")
        client.subscribe("migros/grp2/demo")

        # Blockiert bis zum Empfang von Nachrichten
        print("Warte auf Nachrichten...")
        client.loop_forever()


# Starte die asynchrone Verbindung
asyncio.get_event_loop().run_until_complete(connect_mqtt())






