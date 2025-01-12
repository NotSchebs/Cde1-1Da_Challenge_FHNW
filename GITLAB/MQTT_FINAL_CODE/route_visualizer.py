class RouteVisualizer:
    def __init__(self, map_app, coordinates, humidity_data):
        self.map_app = map_app
        self.coordinates = coordinates
        self.humidity_data = humidity_data
        self.visited_points = set()
        self.start_point_added = False
        self.last_point = None

    def update_markers_and_paths(self, new_coordinates, humidity_data):
        for i, (lat, lon, temp, humidity) in enumerate(new_coordinates):
            current_point = (lat, lon)

            if current_point in self.visited_points:
                continue

            self.visited_points.add(current_point)

            if i == 0 and not self.start_point_added:
                self.map_app.add_marker(lat, lon, f"Start: {humidity}%")
                self.map_app.set_initial_position(lat, lon, zoom=10)
                self.start_point_added = True
            else:
                if humidity != self.humidity_data[-1] if self.humidity_data else True:
                    self.map_app.add_marker(lat, lon, f"Humidity: {humidity}%")
                    self.map_app.set_initial_position(lat, lon, zoom=10)

            if self.last_point:
                self.map_app.add_path([self.last_point, current_point], color=self.get_color(temp))

            self.last_point = current_point
            self.humidity_data.append(humidity)

    @staticmethod
    def get_color(temperature):
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
