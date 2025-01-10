class RouteVisualizer:
    def __init__(self, map_app, coordinates, humidity_data):
        """Initialize with a MapApp instance and route data"""
        self.map_app = map_app
        self.coordinates = coordinates
        self.humidity_data = humidity_data
        self.markers = []  # Keep track of markers
        self.markers_track = []  # Track visited points
        self.hum_record = []  # Keep track of humidity changes
        self.visited_points = set()  # Set to track unique coordinates
        self.start_point_added = False  # Flag to track if the start point is added

    def update_markers_and_paths(self, new_coordinates, humidity_data):
        """Update the map with new coordinates dynamically."""

        for i, (lat, lon, temp, humidity) in enumerate(new_coordinates):
            current_point = (lat, lon)

            # Skip the point if it has been visited already (don't reprocess it)
            if current_point in self.visited_points:
                continue

            # Mark the point as visited
            self.visited_points.add(current_point)

            # Add marker for the first point (start)
            if i == 0 and not self.start_point_added:
                self.map_app.add_marker(lat, lon, f"Start: {humidity}%")
                self.map_app.set_initial_position(lat, lon, zoom=10)  # Set map view on start point
                self.markers_track.append(current_point)
                self.hum_record.append(humidity)
                self.start_point_added = True  # Mark the start point added

            # Add a marker when humidity changes (only if it changed from the previous)
            elif i > 0 and humidity != self.hum_record[-1]:
                self.map_app.add_marker(lat, lon, f"Humidity: {humidity}%")
                self.map_app.set_initial_position(lat, lon, zoom=10)
                self.hum_record.append(humidity)

            # Draw path between consecutive coordinates
            if i > 0:
                prev_lat, prev_lon, _, _ = new_coordinates[i - 1]
                self.map_app.add_path([(prev_lat, prev_lon), (lat, lon)], color=self.get_color(temp))

            # Always track this point for the path history
            self.markers_track.append(current_point)

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
