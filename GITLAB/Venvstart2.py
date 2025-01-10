import sys
import os
import subprocess
import time

def Venvstart():
    # Use the current Python interpreter
    python_executable = sys.executable

    # Copy the current environment variables
    env = os.environ.copy()

    # Ensure that the venv variables are set in the subprocess
    env["VIRTUAL_ENV"] = os.environ.get("VIRTUAL_ENV", "")
    env["PATH"] = os.path.dirname(python_executable) + os.pathsep + env["PATH"]

    # Calling the simulator script in the background
    process = subprocess.Popen(
        [
            python_executable,
            "./simulator.py",
            "./data/demo1.geojson",
            "-c",
            "./config-switch.ini",
        ],
        env=env,
    )

    print(f"Simulator started with PID: {process.pid}")