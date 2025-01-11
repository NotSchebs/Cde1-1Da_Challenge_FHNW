from map_app import MapApp
from route_data import RouteData
from route_visualizer import RouteVisualizer
from plot import Plot
from legend_creator import LegendCreator
from VenvstartMQTT import Venvstart
import threading

if __name__ == "__main__":
    Venvstart()
    # Initialize Map Application
    app = MapApp()

    # Initialize Route Data and MQTT
    route_data = RouteData()

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


    # Function to start MQTT
    def start_mqtt():
        """Start receiving data via MQTT."""
        print("Starting MQTT to receive data...")
        route_data.receive_csv_from_mqtt()

    # Start MQTT in a separate thread
    import threading
    mqtt_thread = threading.Thread(target=start_mqtt, daemon=True)
    mqtt_thread.start()

    # Initialize Visualizer
    visualizer = RouteVisualizer(app, [], [])


    # Create and initialize plot
    plot_updater = Plot([], [])
    plot_updater.initialize_plot(app.root)

    # Initialize LegendCreator
    legend_creator = LegendCreator(app.root, visualizer)
    # Create and display the legend
    legend_creator.erstelle_legende()

    # Schedule the first update
    app.root.after(500, update_visualization)

    # Run the app
    try:
        app.run()
    except KeyboardInterrupt:
        print("Application closed by user.")