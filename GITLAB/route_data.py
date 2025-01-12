import json
import threading
import paho.mqtt.client as mqtt


class RouteData:
    def __init__(self, broker_url, broker_port, company, container, route):
        """Fetch and store route data exclusively via MQTT."""
        self.broker_url = broker_url.strip()
        self.broker_port = broker_port
        self.company = company
        self.container = container
        self.route = route
        self.TOPIC = f"{self.company}/{self.container}/{self.route}"
        self.csv_data = []  # Store CSV data dynamically from MQTT
        self.new_data_available = False  # Flag to indicate new data arrival
        self.lock = threading.Lock()  # Thread lock for thread-safe operations
        print(f"Initialized RouteData with broker: {self.broker_url}, topic: {self.TOPIC}")

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("Connected successfully!")
            client.subscribe(self.TOPIC)
            print(f"Subscribed to topic: {self.TOPIC}")
        else:
            print(f"Connection failed with error code {rc}")

    def on_message(self, client, userdata, msg):
        try:
            print(f"Message received from topic {msg.topic}")
            message = msg.payload.decode()

            # Parse JSON message
            json_data = json.loads(message)
            if "point" not in json_data:
                print("Invalid message format, missing 'point' field")
                return

            # Extract the 'point' field and split it into values
            point_data = json_data["point"].split(",")
            if len(point_data) >= 5:
                row = [
                    json_data.get("company", ""),
                    json_data.get("container", ""),
                    json_data.get("route", ""),
                    point_data[0],  # Timestamp
                    point_data[1],  # Latitude
                    point_data[2],  # Longitude
                    point_data[3],  # Temperature
                    point_data[4],  # Humidity
                ]
                with self.lock:
                    self.csv_data.append(row)
                    self.new_data_available = True
                print(f"Processed row: {row}")
            else:
                print(f"Skipping invalid point data: {json_data['point']}")

        except json.JSONDecodeError as e:
            print(f"Error decoding JSON message: {e}")
        except Exception as e:
            print(f"Error processing the message: {e}")

    def receive_csv_from_mqtt(self):
        client = mqtt.Client(transport="websockets")
        client.on_connect = self.on_connect
        client.on_message = self.on_message

        try:
            print(f"Connecting to MQTT broker at {self.broker_url}:{self.broker_port}...")
            client.connect(self.broker_url, self.broker_port, 60)
            client.loop_forever()
        except Exception as e:
            print(f"Error: {e}")

    def parse_data(self):
        """Parse the MQTT CSV route data into a list of (lat, lon, temperature, humidity) tuples."""
        parsed_data = []
        with self.lock:
            for row in self.csv_data:
                try:
                    lat = float(row[4])
                    lon = float(row[5])
                    temp = float(row[6])
                    humidity = int(row[7])
                    parsed_data.append((lat, lon, temp, humidity))
                except (ValueError, IndexError) as e:
                    print(f"Skipping invalid row: {row} | Error: {e}")

            self.csv_data.clear()
            self.new_data_available = False
        return parsed_data

    def has_new_data(self):
        """Check if new data is available."""
        with self.lock:
            return self.new_data_available
