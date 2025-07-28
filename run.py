"""
Launcher script for theDP (double pendulum) simulator.
This script ensures the src directory is in the Python path and launches the application.
"""

import sys
import os
import shutil

# Get the directory where run.py is located (project root)
script_dir = os.path.dirname(os.path.abspath(__file__))

# Define the path to the src directory
src_path = os.path.join(script_dir, "src")

# Define the path to the data directory (relative to the script_dir)
data_folder_path = os.path.join(script_dir, "data")

# Add the src directory to the Python path
sys.path.insert(0, src_path)

# Change to the src directory so relative paths work correctly for imports within src
os.chdir(src_path)


# Import and run the main application
from animations import pendulum_animation, trajectory_animation, poincare_animation

if __name__ == "__main__":
    folder_name = data_folder_path
    mode_arg = "animate"
    type_arg = "pendulum"

    # --- Start of new logic to clear folder if it exists ---
    if os.path.exists(folder_name):  # Check if the folder exists
        print(f"Folder '{folder_name}' already exists. Clearing its contents...")
        # Remove the folder and its contents
        shutil.rmtree(folder_name)
        # Recreate the empty folder
        os.makedirs(folder_name)
        print(f"Folder '{folder_name}' cleared and recreated.")
    else:
        # Create the folder if it does not exist
        os.makedirs(folder_name)  #
        print(f"Folder '{folder_name}' created successfully.")
    # --- End of new logic ---

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
            poincare_animation(folder_name=folder_name)
        else:
            print(f"Invalid type: {type_arg}")
            sys.exit(1)
    else:
        print(f"Invalid mode: {mode_arg}")
        sys.exit(1)
