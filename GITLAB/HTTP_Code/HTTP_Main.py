from HTTP_MapApp import MapApp
from HTTP_RouteData import RouteData
from HTTP_Route_selector import RouteSelector
from HTTP_Route_visualizer import RouteVisualizer
from HTTP_utils import plot_popup, erstelle_legende


if __name__ == "__main__":
    # Create Map selection popup
    selector = RouteSelector()
    selected_url = selector.map_options()
    print("Selected URL:", selected_url)

    # Initialize Map Application
    app = MapApp()

    # Fetch route data
    route_url = selected_url
    route_data = RouteData(route_url)
    coordinates, humidity_data, temp, LF = route_data.parse_data()

    # Visualize route
    visualizer = RouteVisualizer(app, coordinates, humidity_data)
    visualizer.visualize()

    # Display additional visualizations
    plot_popup(temp, LF)
    erstelle_legende()

    # Run the Tkinter app
    app.run()
