import requests

class RouteData:
    def __init__(self, url):
        self.data = self.fetch_data(url)

    @staticmethod
    def fetch_data(url):
        response = requests.get(url, verify=False)  # Ignore insecure website warnings
        return response.text

    def parse_data(self):
        lines = self.data.strip().split('\n')
        coord = []
        hum_dat = []
        tem = []
        lf = []
        for line in lines:
            values = line.split(',')
            if len(values) == 5:
                _, latitude, longitude, temperature, humidity = values
                if (float(latitude), float(longitude), float(temperature)) in coord:
                    continue
                coord.append((float(latitude), float(longitude), float(temperature)))
                hum_dat.append((float(latitude), float(longitude), int(humidity)))
                tem.append(float(temperature))
                lf.append(float(humidity))
        return coord, hum_dat, tem, lf
