import requests

class RouteData:
    def __init__(self, url):
        """Fetch and store route data from a given URL"""
        self.url = url
        self.data = self.fetch_data(url)

    @staticmethod
    def fetch_data(url):
        """Request data from a URL and return as plain text."""
        try:
            response = requests.get(url, verify=False, timeout=10)  # Set timeout for safety
            response.raise_for_status()  # Raise exception for HTTP errors
            return response.text
        except requests.RequestException as e:
            print(f"Error fetching data from URL: {e}")
            return ""

    def parse_data(self):
        """Parse the CSV route data into a list of (lat, lon, temperature, humidity) tuples"""
        lines = self.data.strip().split("\n")
        parsed_data = []

        for line in lines:
            values = line.split(',')
            if len(values) >= 5:  # Ensure there are at least 5 elements
                try:
                    lat = float(values[1])
                    lon = float(values[2])
                    temp = float(values[3])
                    humidity = int(values[4])
                    parsed_data.append((lat, lon, temp, humidity))
                except ValueError:
                    print(f"Skipping invalid line: {line}")
            else:
                print(f"Skipping incomplete line: {line}")

        print(f"Parsed data: {parsed_data}")
        return parsed_data

