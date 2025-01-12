
# Project: Container Simulator

## Overview
This project is a comprehensive Python application for creating and visualizing route maps, enabling users to:

- Select optimal routes.
- Generate route visualizations.
- Scan profiles and analyze route-related data.
- Integrate real-time MQTT data for dynamic updates.

## Folder Structure and Files

### Root Files
- **`main.py`**: The entry point of the application. Initializes the program and connects all modules.
- **`legend_creator.py`**: Generates legends for route maps to ensure clarity and enhance visualizations.
- **`map_app.py`**: Responsible for map-related functions, including loading and integrating routes.
- **`plot.py`**: Visualizes data and creates route graphs.
- **`profile_scan.py`**: Scans and analyzes profiles related to routes, providing detailed insights into the data.
- **`route_data.py`**: Processes and manages route-related data.
- **`route_selector.py`**: Allows users to select specific routes based on predefined criteria.
- **`route_visualizer.py`**: Creates interactive and user-friendly visualizations for routes.
- **`MQTT_Hartcodiert.py`**: Handles MQTT integration for real-time data reception and updates.
- **`Venvstart.py`**: A utility script for initializing and managing the virtual environment.
- **`requirements.txt`**: Lists the required Python libraries for the project.
- **`.gitignore`**: Specifies files and directories to be ignored by version control.
- **`.name`**: Project name for local development.

### HTTP Simulation Interactive Code (`HTTP_Sim_Interactive_Code`)
This folder contains simulation-specific scripts for interactive HTTP-based simulations.

- **`Sim_Main.py`**: Main script for interactive HTTP simulations.
- **`Sim_map_app.py`**: Simulated map application for testing.
- **`Sim_plot.py`**: Module for visualizing temperature and humidity changes.
- **`Sim_real_time.py`**: Handles real-time simulations and updates.
- **`Sim_route_data.py`**: Processes simulation-related route data.
- **`Sim_route_selector.py`**: Module for selecting routes based on criteria.
- **`Sim_route_visualizer.py`**: Dynamically visualizes routes in simulations.
- **`Sim_util.py`**: Utility functions for simulation-specific tasks.

### HTTP Simulation Interactive Code with Text (`HTTP_Sim_Interactive_mit_txt_Code`)
This folder provides alternative implementations for HTTP simulations using text-based configurations.

- **`routes.csv`**: Contains route data for simulations.
- **`Sim_Main.py`**: Main script for simulations with text-based configurations.
- **`Sim_map_app.py`**: Map module for simulations.
- **`Sim_plot.py`**: Plot module for visualizations.
- **`Sim_real_time.py`**: Real-time simulation module.
- **`Sim_route_data.py`**: Data module for routes.
- **`Sim_route_selector.py`**: Module for selecting routes based on criteria.
- **`Sim_route_visualizer.py`**: Visualizes routes in simulations.
- **`Sim_util.py`**: Utility functions for simulations.
- **`Variable_Server_URL.txt`**: Contains server URLs for simulations.

### HTTP Code (`HTTP_Code`)
This folder contains scripts specifically designed for HTTP-based functionalities of the application.

- **`HTTP_Main.py`**: Main script for managing HTTP operations.
- **`HTTP_MapApp.py`**: Map module for HTTP scenarios.
- **`HTTP_Route_selector.py`**: Module for selecting routes in HTTP applications.
- **`HTTP_Route_visualizer.py`**: Dynamically visualizes routes in HTTP scenarios.
- **`HTTP_RouteData.py`**: Processes and stores route data for HTTP use cases.
- **`HTTP_utils.py`**: Utility functions for HTTP operations.

### GeoJSON Files
These files contain geospatial data for various routes:

- **`demo.geojson`**: Example file for basic tests.
- **`demo1.geojson`**: Detailed example data for simulations.
- **`demo2_extremvieledaten.geojson`**: Data-intensive GeoJSON file.
- **`demo3.geojson`**: Additional example data.
- **`horw-engelberg.geojson`**: Route from Horw to Engelberg.
- **`horw-luzern.geojson`**: Route from Horw to Lucerne.
- **`kriens-horw.geojson`**: Route from Kriens to Horw.
- **`luzern-horw.geojson`**: Route from Lucerne to Horw.
- **`olten-brugg.geojson`**: Route from Olten to Brugg.

### IntelliJ IDEA Project Files
These files support project management in IntelliJ IDEA:

- **`profiles_settings.xml`**: Settings for project inspections.
- **`misc.xml`**: Contains SDK and project information.
- **`modules.xml`**: Manages project modules.
- **`vcs.xml`**: Version control settings (e.g., Git).
- **`GITLAB.iml`**: Module file for IntelliJ IDEA.

### Other Files and Logs
- **`simulator.py`**: Simulates route and MQTT data.
- **`simulator.log`**: Log files for monitoring and debugging.
- **`config-switch.ini`**: Configuration file for HTTP simulations.
- **`configuration.ini`**: Configuration file for MQTT-based simulations.
- **`profile.py`**: Simulates temperature and humidity profiles.
- **`mqtt.py`**: Handles MQTT communication.
- **`http.py`**: Processes HTTP communication.

## Installation and Setup
1. Clone the repository to your local machine.
2. Navigate to the project directory.
3. Run the following commands to set up a virtual environment and install dependencies:
   ```bash
   python Venvstart.py
   source venv/bin/activate  # For Linux/Mac
   venv\Scriptsctivate   # For Windows
   pip install -r requirements.txt
   ```
4. For MQTT-specific functionalities, ensure the simulator and configuration files are properly set up:
   - `simulator.py`
   - `config-switch.ini`

## Execution
1. Ensure the virtual environment is activated.
2. Run the main script to start the application:
   ```bash
   python main.py
   ```
3. To use MQTT functionalities, run `MQTT_Hartcodiert.py`:
   ```bash
   python MQTT_Hartcodiert.py
   ```
4. To use HTTP simulation scripts, navigate to the respective folder and run the desired script, e.g.,:
   ```bash
   cd HTTP_Sim_Interactive_Code
   python Sim_Main.py
   ```
5. For HTTP-based functionalities, run scripts from the `HTTP_Code` folder:
   ```bash
   cd HTTP_Code
   python HTTP_Main.py
   ```

## Features
- **Route Selection**: Choose the best route based on various parameters.
- **Interactive Map Visualizations**: Interact with generated maps.
- **Profile Analysis**: Analyze detailed route profiles.
- **Real-Time MQTT Data Integration**: Visualize real-time data.
- **Customizable Legends**: Add legends to maps.
- **Simulator Integration**: Test and debug with simulated data.
- **Simulation Profiles**: Simulate temperature and humidity changes.
- **Flexible Communication Management**: Use MQTT and HTTP for robust data integration.

## Requirements
- Python 3.8 or higher
- Required Python libraries (see `requirements.txt`)
- Additional configurations for MQTT

## Contributing
1. Fork the repository.
2. Create a new feature branch.
3. Commit your changes with clear messages.
4. Push the branch and create a pull request.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Contact
For questions or support, contact us via [email/communication channel].

