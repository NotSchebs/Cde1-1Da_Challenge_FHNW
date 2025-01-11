import sys
import os
import subprocess
import time

def Venvstart():
    python_executable = sys.executable
    env = os.environ.copy()
    env["VIRTUAL_ENV"] = os.environ.get("VIRTUAL_ENV", "")
    env["PATH"] = os.path.dirname(python_executable) + os.pathsep + env["PATH"]

    try:
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
    except FileNotFoundError as e:
        print(f"File not found: {e}")
    except Exception as e:
        print(f"Error starting simulator: {e}")
