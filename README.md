# Double Pendulum Simulator



A Python-based simulation of a double pendulum system, demonstrating chaotic motion using the Lagrangian equations of motion and high-precision numerical integration.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Physics Background](#physics-background)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

## Introduction

The double pendulum is a classic example of a chaotic system in classical mechanics, known for its extreme sensitivity to initial conditions. This simulator provides an interactive visualization of the double pendulum's dynamics, allowing users to observe its complex and unpredictable motion in real-time. It leverages the Lagrangian formalism to derive the equations of motion and employs advanced numerical integration techniques for accurate simulation.

## Features

* **Lagrangian Dynamics**: Simulates the double pendulum using its full Lagrangian equations of motion, ensuring accurate physical representation.
* **Real-time Animation**: Provides interactive matplotlib animations to visualize the pendulum's motion.
* **Trail Visualization**: Displays the path traced by the lower pendulum's mass over time.
* **Trajectory Plotting**: Visualizes the system's trajectory in a user-definable phase space (e.g., $\theta_1$ vs $\omega_1$, $\theta_2$ vs $p_2$).
* **Poincaré Section**: Computes and plots Poincaré sections to reveal the underlying chaotic or periodic nature of the system's phase space.
* **High-Precision Numerical Integration**: Utilizes SciPy's `solve_ivp` with the 'DOP853' method for robust and accurate integration of the ordinary differential equations.
* **Chaotic Behavior Demonstration**: Highlights the sensitive dependence on initial conditions, a hallmark of chaotic systems.

## Physics Background

The double pendulum consists of two simple pendulums connected in series. It is a canonical example of a system with nonlinear dynamics and chaotic behavior.

The system has two degrees of freedom, typically represented by the angles $\theta_1$ and $\theta_2$ of each pendulum arm with respect to the vertical. The Lagrangian equations of motion are used to describe the system's dynamics:

$$\frac{d}{dt} \left( \frac{\partial L}{\partial \dot{q}_i} \right) - \frac{\partial L}{\partial q_i} = 0$$

For this specific setup (with $M_1=M_2=M$ and $L_1=L_2=L$), the second-order differential equations for $\theta_1$ and $\theta_2$ are:

$$\frac{d^2\theta_1}{dt^2} = \frac{g \sin\theta_2 \cos(\theta_1-\theta_2) - L \sin(\theta_1-\theta_2) (\dot{\theta}_1^2 \cos(\theta_1-\theta_2) + \dot{\theta}_2^2) - 2 g \sin\theta_1}{L (1 + \sin^2(\theta_1-\theta_2))}$$

$$\frac{d^2\theta_2}{dt^2} = \frac{2 (L \dot{\theta}_1^2 \sin(\theta_1-\theta_2) - g \sin\theta_2 + g \sin\theta_1 \cos(\theta_1-\theta_2)) + L \dot{\theta}_2^2 \sin(\theta_1-\theta_2) \cos(\theta_1-\theta_2)}{L (1 + \sin^2(\theta_1-\theta_2))}$$

These are converted into a system of four first-order ODEs for numerical integration: $(\theta_1, \dot{\theta}_1, \theta_2, \dot{\theta}_2)$.

## Requirements

Ensure you have Python 3.7 or newer installed.
The following Python libraries are required:

* `numpy`
* `scipy`
* `matplotlib`
* `tqdm`


## Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/your-username/double-pendulum-simulator.git](https://github.com/your-username/double-pendulum-simulator.git) # Replace with your actual repository URL
    cd double-pendulum-simulator
    ```

2.  **Install dependencies:**
    ```bash
    pip install numpy scipy matplotlib tqdm
    ```
3.  **Install FFmpeg:**
    If you plan to save animations as MP4 files (recommended), you will need FFmpeg installed on your system and accessible via your system's PATH. You can download it from the [official FFmpeg website](https://ffmpeg.org/download.html).

## Usage

Navigate to the root directory of the cloned repository (`double-pendulum-simulator/`).

Run the simulation using the `run.py` launcher script.

1.  **Run Double Pendulum Animation:**
    Displays a real-time animation of the double pendulum's physical motion with a trail for the lower mass.
    ```bash
    python run.py animate pendulum
    ```
    *Output saved to `pendulum_animation.mp4`*

2.  **Run Trajectory Animation:**
    Displays an animation of the system's trajectory in a chosen 2D phase space (e.g., $(\theta_1, \omega_1)$). The specific variables are configured via `i1` and `i2` in `main.py`'s `trajectory_animation()` function.
    ```bash
    python run.py animate trajectory
    ```
    *Output saved to `trajectory_animation.mp4`*

3.  **Compute and Display Poincaré Section:**
    Calculates and plots a Poincaré section, providing insights into the system's long-term behavior. The section is taken at a constant value of a chosen observable, as defined by `i_section` in `main.py`'s `poincare_animation()` function. The displayed coordinates are defined by `i1` and `i2`.
    ```bash
    python run.py animate Poincare
    ```

## Configuration

All simulation parameters can be adjusted directly within `src/main.py`.

* **Physical Constants:**
    * `g = 10` (gravitational acceleration in m/s²)
    * `m1, m2 = 1.0, 1.0` (masses of the pendulum bobs in kg)
    * `L1, L2 = 1.0, 1.0` (lengths of the pendulum arms in meters)

* **Initial Conditions:**
    Initial conditions are determined by the total energy `DeltaE`. The `find_initial_conditions(DeltaE)` function sets `q1_0`, `q2_0`, `omega1_0`, `omega2_0` based on this energy level, handling different initial configurations.

* **Simulation Parameters:**
    * `t_span = (0, tf)`: Tuple defining the simulation duration from 0 to `tf` seconds.
    * `t_eval = np.linspace(*t_span, Np_frames)`: A NumPy array specifying the `Np_frames` time points at which the solution should be stored for animation or plotting.
    * `solve_ivp` parameters: `method`, `rtol`, and `atol` for the numerical solver can be adjusted directly in the function calls within `main.py`.
        * `method="DOP853"` (default in code)
        * `rtol=1e-10` (relative tolerance)
        * `atol=1e-10` (absolute tolerance)

* **Animation Parameters (in `main.py`):**
    * `interval`: Controls the delay between frames for real-time display in milliseconds.
    * `fps`: Frames per second for saved video files (e.g., `ani.save('output.mp4', fps=60)`).
    * `markersize` / `lw` / `alpha`: Visual properties for lines and trails.

* **Trajectory/Poincaré Plotting (in `main.py`):**
    * `i1`, `i2`: Indices (0-5) corresponding to the observables (q1, q2, omega1, omega2, p1, p2) to be plotted on the x and y axes respectively.
    * `i_section`: Index (0-5) of the observable at which the Poincaré section is taken (i.e., when this observable crosses zero).
    * `Np`: Number of points to compute for the Poincaré section.

## Project Structure


```
DP/
├── README.md          # This file
├── run.py             # Launcher script
├── src/
│   └── main.py       # Main simulation code
└── .gitignore        # Git ignore file
```
