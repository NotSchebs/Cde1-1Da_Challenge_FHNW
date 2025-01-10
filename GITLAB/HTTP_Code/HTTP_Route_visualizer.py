
class RouteVisualizer:
    def __init__(self, map_app, coord, hum_data):
        """Initialize with a MapApp instance and route data"""
        self.map_app = map_app
        self.coordinates = coord
        self.humidity_data = hum_data
    @staticmethod
    def get_color(temperature):
        """Determine line color based on temperature"""
        if temperature < 0:
            return 'lightcyan'
        elif 0 <= temperature < 10:
            return 'cyan'
        elif 10 <= temperature < 15:
            return 'mediumspringgreen'
        elif 15 <= temperature < 20:
            return 'springgreen'
        elif 20 <= temperature < 25:
            return 'lime'
        elif 25 <= temperature < 30:
            return 'limegreen'
        elif 30 <= temperature < 35:
            return 'green'
        elif 35 <= temperature < 40:
            return 'tomato'
        elif 40 <= temperature < 45:
            return 'orangered'
        else:
            return 'red'
    def add_markers(self):
        """Add starting, destination, and humidity markers"""
        if self.coordinates:
            start_lat, start_lon, _ = self.coordinates[0]
            end_lat, end_lon, _ = self.coordinates[-1]
            # Starting and destination markers
            self.map_app.add_marker(start_lat, start_lon, f'Starting point! Humidity: {self.humidity_data[0][2]}%')
            self.map_app.add_marker(end_lat, end_lon, f'Destination! Humidity: {self.humidity_data[-1][2]}%')
            self.map_app.set_initial_position(start_lat, start_lon, zoom=10)
            # Humidity markers
            for i in range(len(self.humidity_data) - 1):
                if self.humidity_data[i][2] != self.humidity_data[i + 1][2]:
                    lat, lon, humidity = self.humidity_data[i + 1]
                    self.map_app.add_marker(lat, lon, f'Humidity: {humidity}%')
    def draw_paths(self):
        """Draw paths between coordinates with color indicating temperature"""
        for i in range(1, len(self.coordinates)):
            lat1, lon1, temp1 = self.coordinates[i - 1]
            lat2, lon2, temp2 = self.coordinates[i]
            color = self.get_color(temp1)
            self.map_app.add_path([(lat1, lon1), (lat2, lon2)], color=color)
    def visualize(self):
        """Run visualization by adding markers and drawing paths"""
        self.add_markers()
        self.draw_paths()