from map_app import MapApp
from route_data import RouteData
from route_visualizer import RouteVisualizer
from plot import Plot
from legend_creator import LegendCreator
from route_selector import RouteSelector
from Venvstart2 import Venvstart
from profile_scan import ConfigProfileManager
import threading

if __name__ == "__main__":

    ini_file = 'config-switch.ini'
    profile_file = 'profile.txt'

    # Erstelle eine Instanz der Klasse
    manager = ConfigProfileManager(ini_file, profile_file)
    # Use RouteSelector to get user inputs
    selector = RouteSelector()
    broker_url, company, container, route = selector.map_options()

    # Start the virtual environment (if needed)
    Venvstart(route)


    # Initialize the Map Application
    app = MapApp()

    # Initialize Route Data with selected inputs
    route_data = RouteData(broker_url, 9001, company, container, route)

    # Function to update visualization dynamically
    def update_visualization():
        if route_data.has_new_data():
            parsed_data = route_data.parse_data()
            if parsed_data:
                # Update map visualizer
                visualizer.update_markers_and_paths(parsed_data, visualizer.humidity_data)

                # Extract temperature and humidity data
                temp_data = [point[2] for point in parsed_data]
                humidity_data = [point[3] for point in parsed_data]

                # Update the plot
                plot_updater.update_plot(temp_data, humidity_data)
                print("Plot and map updated with new data.")
        app.root.after(500, update_visualization)

    # Function to start MQTT in a separate thread
    def start_mqtt():
        print("Starting MQTT to receive data...")
        route_data.receive_csv_from_mqtt()

    mqtt_thread = threading.Thread(target=start_mqtt, daemon=True)
    mqtt_thread.start()

    # Initialize Visualizer
    visualizer = RouteVisualizer(app, [], [])

    # Create and initialize the plot
    plot_updater = Plot([], [])
    plot_updater.initialize_plot(app.root)

    # Initialize LegendCreator
    legend_creator = LegendCreator(app.root, visualizer)
    legend_creator.erstelle_legende()

    # Schedule the first visualization update
    app.root.after(500, update_visualization)

    # Run the application
    try:
        app.run()
    except KeyboardInterrupt:
        print("Application closed by user.")
