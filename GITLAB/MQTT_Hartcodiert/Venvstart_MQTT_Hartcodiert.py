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
                os.path.join(".", "..", "simulator.py"),  # simulator.py eine Ebene höher
                os.path.join(".", "..", "data", "demo1.geojson"),  # GeoJSON-Datei als 'file'-Argument
                "--config",
                os.path.join(".", "..", "config-switch.ini"),  # INI-Datei als '--config'-Argument
            ],
            env=env,
        )
        print(f"Simulator started with PID: {process.pid}")
    except FileNotFoundError as e:
        print(f"File not found: {e}")
    except Exception as e:
        print(f"Error starting simulator: {e}")
