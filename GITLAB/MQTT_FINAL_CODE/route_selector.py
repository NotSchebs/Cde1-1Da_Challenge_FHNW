import tkinter as tk
from tkinter import messagebox
import pandas as pd

class RouteSelector:
    def __init__(self, options=None):
        """Initialize the selector with route options."""
        self.server_option = self.load_server_url()  # Default server URL loaded from file
        self.default_options = self.load_routes_from_csv()  # Load routes from CSV file
        self.options = options if options is not None else self.default_options
        self.selected_server = None  # Selected server URL
        self.selected_route_data = None  # Selected route details

    @staticmethod
    def load_server_url():
        """Load the server URL from a configuration file."""
        try:
            with open('Variable_Server_URL.txt', 'r') as file:
                for line in file:
                    if line.startswith("httpadresse="):
                        server_url = line.split('=')[1].strip().strip("'")
                        print(f"Loaded server URL: {server_url}")  # Debug statement
                        return server_url
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
                {
                    "route_name": row["route_name"],
                    "company": row["Company"],
                    "container": row["Container"],
                }
                for _, row in routes_df.iterrows()
            ]
            print(f"Loaded routes: {routes}")  # Debug statement
            return routes
        except FileNotFoundError:
            messagebox.showerror("Error", "Routes CSV file not found. Exiting...")
            raise SystemExit("Routes CSV file not found.")
        except Exception as e:
            messagebox.showerror("Error", f"Error reading routes CSV file: {e}")
            raise SystemExit(f"Error reading routes CSV file: {e}")

    def submit_server_selection(self, var, server_popup, custom_entry):
        """Handle the submission of the selected server option or custom server URL."""
        selected_option = var.get()

        if selected_option == "Custom Server URL":
            custom_url = custom_entry.get().strip()
            if custom_url:
                self.selected_server = custom_url
                print(f"Custom server URL selected: {self.selected_server}")  # Debug statement
                server_popup.destroy()
            else:
                messagebox.showwarning("Invalid URL", "Please enter a valid server URL.")
        elif selected_option:
            self.selected_server = selected_option
            print(f"Server URL selected: {self.selected_server}")  # Debug statement
            server_popup.destroy()
        else:
            messagebox.showwarning("No selection", "Please select a server or enter a custom URL.")

    def select_server(self):
        """Create the popup to select or input the server URL."""
        server_popup = tk.Tk()
        server_popup.title("Select Server")

        var = tk.StringVar(value="")

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

        custom_entry = tk.Entry(server_popup)
        custom_entry.pack(anchor="w", padx=20, pady=5)

        submit_button = tk.Button(
            server_popup,
            text="Submit",
            command=lambda: self.submit_server_selection(var, server_popup, custom_entry)
        )
        submit_button.pack(pady=20)

        server_popup.wait_window()

    def submit_route_selection(self, var, route_popup):
        """Handle the submission of the selected route option."""
        selected_option = var.get()

        if selected_option == "Custom Map URL":
            route_popup.destroy()
            self.open_custom_url_popup()
        elif selected_option.isdigit():
            self.selected_route_data = self.options[int(selected_option)]
            print(f"Route selected: {self.selected_route_data}")  # Debug statement
            route_popup.destroy()
        else:
            messagebox.showwarning("No selection", "Please select a route.")

    def select_route(self):
        """Create the popup to select a route."""
        route_popup = tk.Tk()
        route_popup.title("Select Route")

        var = tk.StringVar(value="")

        for idx, route in enumerate(self.options):
            label = f"{route['route_name']} ({route['company']}/{route['container']})"
            tk.Radiobutton(route_popup, text=label, variable=var, value=str(idx)).pack(anchor="w")

        tk.Radiobutton(
            route_popup, text="Custom Map URL", variable=var, value="Custom Map URL"
        ).pack(anchor="w")

        submit_button = tk.Button(
            route_popup,
            text="Submit",
            command=lambda: self.submit_route_selection(var, route_popup)
        )
        submit_button.pack(pady=20)

        route_popup.wait_window()

    def open_custom_url_popup(self):
        """Open a new popup to input a custom route with multiple fields."""
        custom_popup = tk.Tk()
        custom_popup.title("Enter Custom Route Details")

        tk.Label(custom_popup, text="Route Name:").pack(anchor="w", padx=10, pady=2)
        route_entry = tk.Entry(custom_popup, width=40)
        route_entry.pack(anchor="w", padx=10, pady=2)

        tk.Label(custom_popup, text="Company:").pack(anchor="w", padx=10, pady=2)
        company_entry = tk.Entry(custom_popup, width=40)
        company_entry.pack(anchor="w", padx=10, pady=2)

        tk.Label(custom_popup, text="Container:").pack(anchor="w", padx=10, pady=2)
        container_entry = tk.Entry(custom_popup, width=40)
        container_entry.pack(anchor="w", padx=10, pady=2)

        def handle_action(save):
            route = route_entry.get().strip()
            company = company_entry.get().strip()
            container = container_entry.get().strip()

            if all([route, company, container]):
                self.selected_route_data = {
                    "route_name": route,
                    "company": company,
                    "container": container,
                }
                print(f"Custom Route Details: {self.selected_route_data}")

                if save:
                    self.save_custom_route(route, company, container)

                custom_popup.destroy()
            else:
                messagebox.showwarning("Incomplete Details", "Please fill in all fields.")

        tk.Button(
            custom_popup, text="Run Once", command=lambda: handle_action(save=False)
        ).pack(pady=5)

        tk.Button(
            custom_popup, text="Save and Run", command=lambda: handle_action(save=True)
        ).pack(pady=5)

        custom_popup.mainloop()

    def save_custom_route(self, route, company, container):
        """Save the custom route to the CSV file."""
        try:
            csv_file = 'routes.csv'
            routes_df = pd.read_csv(csv_file)
            new_row = {
                'route_name': route,
                'Company': company,
                'Container': container
            }
            routes_df = pd.concat([routes_df, pd.DataFrame([new_row])], ignore_index=True)
            routes_df.to_csv(csv_file, index=False)
            messagebox.showinfo("Success", "Custom route saved successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save custom route: {e}")

    def map_options(self):
        """Main method to run server selection and then route selection."""
        self.select_server()

        if not self.selected_server:
            messagebox.showerror("Error", "Server selection failed.")
            raise SystemExit("Server selection failed.")

        self.select_route()

        if not self.selected_route_data:
            messagebox.showerror("Error", "Route selection failed.")
            raise SystemExit("Route selection failed.")

        return (
            self.selected_server,
            self.selected_route_data["company"],
            self.selected_route_data["container"],
            self.selected_route_data["route_name"],
        )
