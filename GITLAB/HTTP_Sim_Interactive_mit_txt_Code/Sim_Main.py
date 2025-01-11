from Sim_map_app import MapApp
from Sim_route_data import RouteData
from Sim_route_selector import RouteSelector
from Sim_route_visualizer import RouteVisualizer
from Sim_plot import Plot
from Sim_util import erstelle_legende, simulate_real_time_updates

if __name__ == "__main__":
    # Create Map selection popup
    selector = RouteSelector()
    selected_url = selector.map_options()

    if not selected_url:
        print("No route selected. Exiting...")
        exit(1)

    print("Final Selected URL:", selected_url)

    # Fetch data
    route_data = RouteData(selected_url)
    full_data = route_data.parse_data()

    if not full_data:
        print("No data fetched for the selected route. Exiting...")
        exit(1)

    # Initialize Map Application
    app = MapApp()

    # Visualize route
    visualizer = RouteVisualizer(app, [], [])
    plot_updater = Plot([], [])

    # Initialize the plot popup
    plot_updater.initialize_plot(app.root)
    erstelle_legende()

    simulate_real_time_updates(app, visualizer, plot_updater, full_data)

    # Run the app
    app.run()

