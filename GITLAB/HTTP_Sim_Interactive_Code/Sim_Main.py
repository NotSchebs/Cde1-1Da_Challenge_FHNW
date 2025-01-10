from Sim_map_app import MapApp
from Sim_route_data import RouteData
from Sim_route_selector import RouteSelector
from Sim_route_visualizer import RouteVisualizer
from Sim_plot import Plot
from Sim_util import erstelle_legende, simulate_real_time_updates, simulate_real_time_updates

if __name__ == "__main__":

    #create Map selection popup
    selector = RouteSelector()
    selected_url = selector.map_options()
    print("Selected URL:", selected_url)

    # Fetch data
    route_data = RouteData(selected_url)
    full_data = route_data.parse_data()

    # Initialize Map Application
    app = MapApp()

    # Visualize route
    visualizer = RouteVisualizer(app, [], [])
    plot_updater = Plot([], [])

    # Abbildung anzeigen
    # Initialize the plot popup
    plot_updater.initialize_plot(app.root)
    erstelle_legende()

    simulate_real_time_updates(app, visualizer, plot_updater, full_data)

    # Run the app
    app.run()