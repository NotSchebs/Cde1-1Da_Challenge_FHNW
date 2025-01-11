import tkinter as tk
from tkinter import messagebox
import re
import pandas as pd

class RouteSelector:
    def __init__(self, options=None):
        """Initialize the selector with route options.
        Default options are used if none are provided.
        """
        self.server_option = self.load_server_url()  # Default server URL loaded from file
        self.default_options = self.load_routes_from_csv()  # Load routes from CSV file
        # Use provided options if available; otherwise, use default options
        self.options = options if options is not None else self.default_options
        self.selected_server = self.server_option
        self.selected_url = None  # Store the selected route URL

    @staticmethod
    def load_server_url():
        """Load the server URL from a configuration file."""
        try:
            with open('Variable_Server_URL.txt', 'r') as file:
                for line in file:
                    if line.startswith("httpadresse="):
                        return line.split('=')[1].strip().strip("'")
        except FileNotFoundError:
            messagebox.showerror("Error", "Configuration file not found. Exiting...")
            raise SystemExit("Configuration file not found.")
        except Exception as e:
            messagebox.showerror("Error", f"Error reading configuration file: {e}")
            raise SystemExit(f"Error reading configuration file: {e}")

    @staticmethod
    def load_routes_from_csv():
        """Load route options from a CSV file."""
        try:
            csv_file = 'routes.csv'
            routes_df = pd.read_csv(csv_file)
            routes = [
                (row['route_name'], f"{row['route_path']}")
                for _, row in routes_df.iterrows()
            ]
            return routes
        except FileNotFoundError:
            messagebox.showerror("Error", "Routes CSV file not found. Exiting...")
            raise SystemExit("Routes CSV file not found.")
        except Exception as e:
            messagebox.showerror("Error", f"Error reading routes CSV file: {e}")
            raise SystemExit(f"Error reading routes CSV file: {e}")

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

    def submit_route_selection(self, var, route_popup):
        """Handle the submission of the selected route option or open a custom URL popup."""
        selected_option = var.get()

        if selected_option == "Custom Map URL":
            route_popup.destroy()
            self.open_custom_url_popup()
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

        # Submit button to confirm route selection
        submit_button = tk.Button(
            route_popup,
            text="Submit",
            command=lambda: self.submit_route_selection(var, route_popup)
        )
        submit_button.pack(pady=20)

        route_popup.wait_window()

    def open_custom_url_popup(self):
        """Open a new popup to input a custom route URL with multiple fields."""
        custom_popup = tk.Tk()
        custom_popup.title("Enter Custom Route Details")

        tk.Label(custom_popup, text="Route Name:").pack(anchor="w", padx=10, pady=2)
        route_entry = tk.Entry(custom_popup, width=40)
        route_entry.pack(anchor="w", padx=10, pady=2)

        tk.Label(custom_popup, text="Company:").pack(anchor="w", padx=10, pady=2)
        company_entry = tk.Entry(custom_popup, width=40)
        company_entry.pack(anchor="w", padx=10, pady=2)

        tk.Label(custom_popup, text="Route Path:").pack(anchor="w", padx=10, pady=2)
        route_address_entry = tk.Entry(custom_popup, width=40)
        route_address_entry.pack(anchor="w", padx=10, pady=2)

        tk.Label(custom_popup, text="Container:").pack(anchor="w", padx=10, pady=2)
        container_entry = tk.Entry(custom_popup, width=40)
        container_entry.pack(anchor="w", padx=10, pady=2)

        # Option buttons for actions
        tk.Button(
            custom_popup,
            text="Run Once",
            command=lambda: self.handle_custom_route(route_entry, company_entry, route_address_entry, container_entry, save=False, popup=custom_popup)
        ).pack(pady=5)

        tk.Button(
            custom_popup,
            text="Run and Save",
            command=lambda: self.handle_custom_route(route_entry, company_entry, route_address_entry, container_entry, save=True, popup=custom_popup)
        ).pack(pady=5)

        custom_popup.mainloop()

    def submit_custom_route(self, route, company, route_path, container):
        """Submit the custom route for immediate use in the program."""
        print("Submitting the custom route for immediate use:")
        print(f"Route Name: {route}\nCompany: {company}\nRoute Path: {route_path}\nContainer: {container}")
        # Hier kannst du die Daten weiterleiten, z. B. an die Karte oder andere Komponenten
        self.selected_url = route_path  # Sicherstellen, dass die Route URL korrekt gesetzt ist

    def handle_custom_route(self, route_entry, company_entry, route_address_entry, container_entry, save, popup):
        """Handle custom route input, optionally saving it to the CSV file."""
        route = route_entry.get().strip()
        company = company_entry.get().strip()
        route_path = route_address_entry.get().strip()
        container = container_entry.get().strip()

        if all([route, company, route_path, container]):
            print(
                f"Custom Route Details:\nRoute Name: {route}\nCompany: {company}\nRoute Path: {route_path}\nContainer: {container}")

            # Ensure the route path is complete by adding the server prefix
            full_route_path = self.selected_server + route_path if not route_path.startswith("http") else route_path
            self.selected_url = full_route_path

            if save:
                self.save_custom_route(route, company, full_route_path, container)

            # Prevent duplicate entries in self.options
            if (route, full_route_path) not in self.options:
                self.options.append((route, full_route_path))
                print("Options updated:", self.options)

            popup.destroy()  # Close the popup after handling input
        else:
            messagebox.showwarning("Incomplete Details", "Please fill in all fields.")

    def save_custom_route(self, route, company, route_path, container):
        """Save the custom route to the CSV file."""
        try:
            csv_file = 'routes.csv'
            routes_df = pd.read_csv(csv_file)
            new_row = {
                'route_name': route,
                'Company': company,
                'route_path': route_path,
                'Container': container
            }
            routes_df = pd.concat([routes_df, pd.DataFrame([new_row])], ignore_index=True)
            routes_df.to_csv(csv_file, index=False)
            messagebox.showinfo("Success", "Custom route saved successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save custom route: {e}")

    def map_options(self):
        """Main method to run server selection and then route selection."""
        # First, select the server
        self.select_server()

        if not self.selected_server:
            messagebox.showerror("Error", "Server selection failed.")
            raise SystemExit("Server selection failed.")

        # Update route URLs with the selected server
        self.options = [
            (label, self.selected_server + url if not url.startswith("http") else url)
            for label, url in self.default_options
        ]

        # Then, select the route
        self.select_route()

        if not self.selected_url:
            messagebox.showerror("Error", "Route selection failed.")
            raise SystemExit("Route selection failed.")

        print(f"Using route URL for map: {self.selected_url}")
        return self.selected_url


