'''import paho.mqtt.client as mqtt

# Konfiguration
BROKER_URL = "fl-17-240.zhdk.cloud.switch.ch"
BROKER_PORT = 9001  # Standard-Port für unverschlüsselte MQTT-Verbindungen
TOPIC = "test/topic"  # Beispiel-Topic, ändern je nach Bedarf

# Callback-Funktion, die beim Verbindungsaufbau aufgerufen wird
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Verbindung erfolgreich!")
        # Abonnieren eines Topics nach erfolgreicher Verbindung
        client.subscribe(TOPIC)
    else:
        print(f"Verbindung fehlgeschlagen mit Fehlercode {rc}")

# Callback-Funktion, die aufgerufen wird, wenn eine Nachricht empfangen wird
def on_message(client, userdata, msg):
    print(f"Nachricht empfangen: {msg.topic} -> {msg.payload.decode()}")

# MQTT-Client initialisieren
client = mqtt.Client()

# Callbacks setzen
client.on_connect = on_connect
client.on_message = on_message

# Verbindung zum Broker herstellen
try:
    client.connect(BROKER_URL, BROKER_PORT, 60)
    print("Verbindung wird aufgebaut...")
    # Netzwerk-Loop starten, um Nachrichten zu empfangen
    client.loop_forever()
except Exception as e:
    print(f"Fehler beim Verbindungsaufbau: {e}")
'''
import paho.mqtt.client as mqtt

# Konfiguration
BROKER_URL = "fl-17-240.zhdk.cloud.switch.ch"
BROKER_PORT = 9001  # Standard-Port für unverschlüsselte MQTT-Verbindungen

# Callback-Funktion, die beim Verbindungsaufbau aufgerufen wird
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Verbindung erfolgreich!")
    else:
        print(f"Verbindung fehlgeschlagen mit Fehlercode {rc}")

# MQTT-Client initialisieren
client = mqtt.Client()

# Callback setzen
client.on_connect = on_connect

# Verbindung zum Broker herstellen
try:
    client.connect(BROKER_URL, BROKER_PORT, 60)
    print("Verbindung wird aufgebaut...")
    # Netzwerk-Loop starten
    client.loop_start()
    input("Drücke Enter, um die Verbindung zu beenden...\n")
    client.loop_stop()
    client.disconnect()
except Exception as e:
    print(f"Fehler beim Verbindungsaufbau: {e}")
