import tkinter as tk
from tkinter import messagebox
import re

class RouteSelector:
    def __init__(self, options=None):
        """Initialize the selector with route options.
        Default options are used if none are provided.
        """
        self.server_option = 'https://fl-17-240.zhdk.cloud.switch.ch/'  # Default server URL
        self.default_options = [
            ('Route Map demo1',
             self.server_option + 'containers/grp2/routes/demo?start=0&end=-1&format=csv'),
            ('Route Map demo2',
             self.server_option + 'containers/grp2/routes/demo2_extremvieledaten?start=0&end=-1&format=csv')
        ]
        # Use provided options if available; otherwise, use default options
        self.options = options if options is not None else self.default_options
        self.selected_server = self.server_option
        self.selected_url = None  # Store the selected route URL

    @staticmethod
    def is_valid_url(url):
        """Validate the URL using a regular expression."""
        url_regex = re.compile(
            r'^(?:http|https)://'  # http:// or https://
            r'(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}'  # domain
            r'(?::\d{2,5})?'  # optional port
            r'(?:[/?#]\S*)?$', re.IGNORECASE  # path/query fragment
        )
        return re.match(url_regex, url) is not None

    def submit_server_selection(self, var, server_popup, custom_entry):
        """Handle the submission of the selected server option or custom server URL."""
        selected_option = var.get()

        if selected_option == "Custom Server URL":
            custom_url = custom_entry.get().strip()
            if self.is_valid_url(custom_url):
                self.selected_server = custom_url
                server_popup.destroy()
            else:
                messagebox.showwarning("Invalid URL", "Please enter a valid server URL.")
        elif selected_option:
            self.selected_server = selected_option
            server_popup.destroy()
        else:
            messagebox.showwarning("No selection", "Please select a server or enter a custom URL.")

    def select_server(self):
        """Create the popup to select or input the server URL."""
        server_popup = tk.Tk()
        server_popup.title("Select Server")

        # Variable to store the selected option
        var = tk.StringVar(value="")

        # Radio buttons for default server and custom server
        tk.Radiobutton(
            server_popup,
            text=f"Original Server: {self.server_option}",
            variable=var,
            value=self.server_option
        ).pack(anchor="w")

        tk.Radiobutton(
            server_popup,
            text="Custom Server URL",
            variable=var,
            value="Custom Server URL"
        ).pack(anchor="w")

        # Entry box for custom server input
        custom_entry = tk.Entry(server_popup)
        custom_entry.pack(anchor="w", padx=20, pady=5)

        # Submit button to confirm server selection
        submit_button = tk.Button(
            server_popup,
            text="Submit",
            command=lambda: self.submit_server_selection(var, server_popup, custom_entry)
        )
        submit_button.pack(pady=20)

        server_popup.wait_window()

    def submit_route_selection(self, var, route_popup, custom_entry):
        """Handle the submission of the selected route option or custom route URL."""
        selected_option = var.get()

        if selected_option == "Custom Map URL":
            custom_url = custom_entry.get().strip()
            if self.is_valid_url(custom_url):
                self.selected_url = custom_url
                route_popup.destroy()
            else:
                messagebox.showwarning("Invalid URL", "Please enter a valid route URL.")
        elif selected_option:
            self.selected_url = selected_option
            route_popup.destroy()
        else:
            messagebox.showwarning("No selection", "Please select a route or enter a custom URL.")

    def select_route(self):
        """Create the popup to select a route or enter a custom route URL."""
        route_popup = tk.Tk()
        route_popup.title("Select Route")

        # Variable to store the selected option
        var = tk.StringVar(value="")

        # Radio buttons for route options
        for label, url in self.options:
            tk.Radiobutton(route_popup, text=label, variable=var, value=url).pack(anchor="w")

        # Radio button for custom route URL
        tk.Radiobutton(route_popup, text="Custom Map URL", variable=var, value="Custom Map URL").pack(anchor="w")

        # Entry box for custom route input
        custom_entry = tk.Entry(route_popup)
        custom_entry.pack(anchor="w", padx=20, pady=5)

        # Submit button to confirm route selection
        submit_button = tk.Button(
            route_popup,
            text="Submit",
            command=lambda: self.submit_route_selection(var, route_popup, custom_entry)
        )
        submit_button.pack(pady=20)

        route_popup.wait_window()

    def map_options(self):
        """Main method to run server selection and then route selection."""
        # First, select the server
        self.select_server()

        if not self.selected_server:
            messagebox.showerror("Error", "Server selection failed.")
            return None

        # Update route URLs with the selected server
        self.options = [
            (label, url.replace(self.server_option, self.selected_server))
            for label, url in self.default_options
        ]

        # Then, select the route
        self.select_route()

        if not self.selected_url:
            messagebox.showerror("Error", "Route selection failed.")
            return None

        return self.selected_url