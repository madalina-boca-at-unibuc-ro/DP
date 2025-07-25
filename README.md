# Double Pendulum Simulator

A Python-based simulation of a double pendulum system using Hamiltonian mechanics and numerical integration. This project demonstrates chaotic motion in classical mechanics through an interactive animation.

## Overview

The double pendulum is a classic example of a chaotic system in classical mechanics. Even with simple initial conditions, the motion becomes unpredictable due to the nonlinear coupling between the two pendulums. This simulator uses the Lagrangian equations of motion to accurately model the system's dynamics.

## Features

- **Lagrangian Dynamics**: Uses the full Lagrangian equations of motion for accurate physics simulation
- **Real-time Animation**: Interactive matplotlib animation showing the pendulum motion
- **Trail Visualization**: Shows the path of the lower pendulum mass over time
- **Numerical Integration**: Uses SciPy's `solve_ivp` with DOP853 method for high-precision integration
- **Chaotic Behavior**: Demonstrates the sensitive dependence on initial conditions characteristic of chaotic systems

## Physics Background

The double pendulum consists of two simple pendulums connected in series. The system has two degrees of freedom (angles θ₁ and θ₂) and exhibits:

- **Nonlinear Dynamics**: The equations of motion are coupled and nonlinear
- **Chaotic Motion**: Small changes in initial conditions lead to dramatically different trajectories
- **Energy Conservation**: The total mechanical energy remains constant (in the absence of friction)

The Lagrangian equations used in this simulation are:

```
θ₁'' = (f₁ - α₁f₂) / (1 - α₁α₂)
θ₂'' = (f₂ - α₂f₁) / (1 - α₁α₂)
```

Where the coupling terms depend on the relative positions and velocities of the two pendulums.

## Requirements

- Python 3.7+
- NumPy
- SciPy
- Matplotlib
- Tqdm

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd DP
```

2. Install the required dependencies:
```bash
pip install numpy scipy matplotlib tqdm
```

## Usage

Run the simulation using one of the following:

```bash
python run.py animate pendulum
```

This will:
1. Set up the Python path to include the `src` directory
2. Launch the double pendulum animation
3. Display the real-time motion with a trail showing the path of the lower mass

OR

```bash
python run.py animate trajectory
```

This will:
1. Set up the Python path to include the `src` directory
2. Launch the double pendulum trajectory animation
3. Display the motion of the representative point in the space $o_1$, $o_2$ in its time evolution. $o_1$ and $o_2$ are chosen from $\theta_1$, $\theta_2$, $\omega_1$, $\omega_2$, $p_1$, $p_2$ through the variables `i1`, `i2` in the trajectory_animation() function.



```bash
python run.py animate Poincare
```

This will:
1. Set up the Python path to include the `src` directory
2. Launch the double pendulum trajectory calculation 
4. Compute `Np` points from the Poincare map in the coordinates $o_1$, $o_2$ at constant $o_p$; $o_1$, $o_2$, $o_p$ can be chosen from  $\theta_1$, $\theta_2$, $\omega_1$, $\omega_2$, $p_1$, $p_2$ through the variables `i1`, `i2`, `i_section` in the trajectory_Poincare() function.


## Configuration

The simulation parameters can be modified in `src/main.py`:

- **Physical Constants**:
  - `g = 10` m/s² (gravitational acceleration)
  - `m₁, m₂ = 1.0, 1.0` kg (masses)
  - `L₁, L₂ = 1.0, 1.0` m (lengths)

- **Initial Conditions**:
    are fixed through the total energy DeltaE

- **Simulation Parameters**:
  - `t_span = (0, tf)`  `tf` seconds (simulation duration)
  - `t_eval = np.linspace(*t_span, np)` ( `np` time points for integration)

## Project Structure

```
DP/
├── README.md          # This file
├── run.py             # Launcher script
├── src/
│   └── main.py       # Main simulation code
└── .gitignore        # Git ignore file
```
