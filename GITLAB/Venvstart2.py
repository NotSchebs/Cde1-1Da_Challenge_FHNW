import sys
import os
import subprocess

def Venvstart(route):
    """
    Start the virtual environment and run the simulator with the specified route.
    """
    python_executable = sys.executable
    env = os.environ.copy()
    env["VIRTUAL_ENV"] = os.environ.get("VIRTUAL_ENV", "")
    env["PATH"] = os.path.dirname(python_executable) + os.pathsep + env["PATH"]

    try:
        process = subprocess.Popen(
            [
                python_executable,
                "./simulator.py",
                f"./data/{route}.geojson",  # Dynamic route
                "-c",
                "./config-switch.ini",
            ],
            env=env,
        )
        print(f"Simulator started with PID: {process.pid}, using route: {route}")
    except FileNotFoundError as e:
        print(f"File not found: {e}")
    except Exception as e:
        print(f"Error starting simulator: {e}")
