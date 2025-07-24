#!/home/madalina/soft/py_env/bin/python3
"""
Launcher script for the SRT (Special Relativity Theory) simulator.
This script ensures the src directory is in the Python path and launches the application.
"""

import sys
import os

# Add the src directory to the Python path
src_path = os.path.join(os.path.dirname(__file__), "src")
sys.path.insert(0, src_path)

# Change to the src directory so relative paths work correctly
os.chdir(src_path)

# Import and run the main application
from main import pendulum_animation, trajectory_animation, poincare_animation

if __name__ == "__main__":
    mode_arg = "plot"
    type_arg = "pendulum"

    if len(sys.argv) > 1:
        mode_arg = sys.argv[1]
        if len(sys.argv) > 2:
            type_arg = sys.argv[2]

    if mode_arg == "animate":
        if type_arg == "pendulum":
            pendulum_animation()
        elif type_arg == "trajectory":
            trajectory_animation()
        elif type_arg == "Poincare":
            poincare_animation()
        else:
            print(f"Invalid type: {type_arg}")
            sys.exit(1)
    elif mode_arg == "plot":
        pass
    else:
        print(f"Invalid mode: {mode_arg}")
        sys.exit(1)
