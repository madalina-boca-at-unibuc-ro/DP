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


## Physics Background



### The double pendulum in the Lagrangian formalism

We consider two the masses $m_1$ and $m_2$ attached to two rigid rods of
length $l_1$ and $l_2$ respectively.

The generalized coordinates of the double pendulum are the angles
$\theta_1$ and $\theta_2$ of the two pendulums. The cartesian
coordinates of the masses are given by: 

$ x_1=l_1 \sin \theta_1                 $

 $x_2=l_1 \sin \theta_1+l_2 \sin \theta_2  $

 $ y_1=-l_1 \cos \theta_1              $

 $ y_2=-l_1 \cos \theta_1-l_2 \cos \theta_2$

The velocities of the masses are given by: 

$ \dot{x}_1=l_1 \dot{\theta}_1 \cos \theta_1      $ 

$ \dot{x}_2=l_1 \dot{\theta}_1 \cos \theta_1+l_2 \dot{\theta}_2 \cos \theta_2$

 $ \dot{y}_1=l_1 \dot{\theta}_1 \sin \theta_1         $
 
  $ \dot{y}_2=l_1 \dot{\theta}_1 \sin \theta_1+l_2 \dot{\theta}_2 \sin \theta_2$ 
  
  The kinetic energy of the double pendulum is given by:

$T = \frac{1}{2}m_1\dot{x}_1^2 + \frac{1}{2}m_2\dot{x}_2^2 + \frac{1}{2}m_1\dot{y}_1^2 + \frac{1}{2}m_2\dot{y}_2^2$

and the potential energy is given by:
 $  V  =m_1 g y_1+m_2 g y_2                     =-m_1 g l_1 \cos \theta_1-m_2 g\left(l_1 \cos \theta_1+l_2 \cos \theta_2\right)  =-\left(m_1+m_2\right) g l_1 \cos \theta_1-m_2 g l_2 \cos \theta_2
$ 

The Lagrangian of the double pendulum is given by:
$$L = T-V = \frac{1}{2}\left(m_1+m_2\right) l_1^2 \dot{\theta}_1^2 + \frac{1}{2} m_2 l_2^2 \dot{\theta}_2^2+m_2 l_1 l_2 \dot{\theta}_1 \dot{\theta}_2 \cos \left(\theta_1-\theta_2\right) + \left(m_1+m_2\right) g l_1 \cos \theta_1+m_2 g l_2 \cos \theta_2$$

### The equations of motion

The equations of motion of the double pendulum are: $$\begin{aligned}
      \frac{d}{dt}\left(\frac{\partial L}{\partial \dot{\theta}_i}\right)-\frac{\partial L}{\partial \theta_i}=0 \quad i=1,2
\end{aligned}$$ The generalized momenta are given by: $$\begin{aligned}
       & p_{\theta_1}=\frac{\partial L}{\partial \dot{\theta}_1}=\left(m_1+m_2\right) l_1^2 \dot{\theta}_1+m_2 l_1 l_2 \dot{\theta}_2 \cos \left(\theta_1-\theta_2\right) \\
       & p_{\theta_2}=\frac{\partial L}{\partial \dot{\theta}_2}=m_2 l_2^2 \dot{\theta}_2+m_2 l_1 l_2 \dot{\theta}_1 \cos \left(\theta_1-\theta_2\right)
\end{aligned}$$ and their time derivatives are given by: $$\begin{aligned}
      \frac{d p_{\theta_1}}{d t}= & \left(m_1+m_2\right) l_1^2 \ddot{\theta}_1+m_2 l_1 l_2 \ddot{\theta}_2 \cos \left(\theta_1-\theta_2\right)  -m_2 l_1 l_2 \dot{\theta}_2 \dot{\theta}_1 \sin \left(\theta_1-\theta_2\right)+m_2 l_1 l_2 \dot{\theta}_2^2 \sin \left(\theta_1-\theta_2\right) \\
      \frac{d p_{\theta_2}}{d t}= & m_2 l_2^2 \ddot{\theta}_2+m_2 l_1 l_2 \ddot{\theta}_1 \cos \left(\theta_1-\theta_2\right)   -m_2 l_1 l_2 \dot{\theta}_1^2 \sin \left(\theta_1-\theta_2\right)+m_2 l_1 l_2 \dot{\theta}_1 \dot{\theta}_2 \sin \left(\theta_1-\theta_2\right)
\end{aligned}$$ Also using the derivatives of the Lagrangian with
respect to the coordinates $$\begin{aligned}
       & \frac{\partial L}{\partial \theta_1}=-m_2 l_1 l_2 \dot{\theta}_1 \dot{\theta}_2 \sin \left(\theta_1-\theta_2\right)-\left(m_1+m_2\right) g l_1 \sin \theta_1 \\
       & \frac{\partial L}{\partial \theta_2}=m_2 l_1 l_2 \dot{\theta}_1 \dot{\theta}_2 \sin \left(\theta_1-\theta_2\right)-m_2 g l_2 \sin \theta_2
\end{aligned}$$ We can write the equations of motion as: $$\begin{aligned}
       & \left(m_1+m_2\right) l_1^2 \ddot{\theta}_1+m_2 l_1 l_2 \ddot{\theta}_2 \cos \left(\theta_1-\theta_2\right)-m_2 l_1 l_2 \dot{\theta}_2 \dot{\theta}_1 \sin \left(\theta_1-\theta_2\right)+m_2 l_1 l_2 \dot{\theta}_2^2 \sin \left(\theta_1-\theta_2\right) \nonumber \\
       & \qquad   = -m_2 l_1 l_2 \dot{\theta}_1 \dot{\theta}_2 \sin \left(\theta_1-\theta_2\right)-\left(m_1+m_2\right) g l_1 \sin \theta_1                                                                                                                                  \\
       & m_2 l_2^2 \ddot{\theta}_2+m_2 l_1 l_2 \ddot{\theta}_1 \cos \left(\theta_1-\theta_2\right)   -m_2 l_1 l_2 \dot{\theta}_1^2 \sin \left(\theta_1-\theta_2\right)+m_2 l_1 l_2 \dot{\theta}_1 \dot{\theta}_2 \sin \left(\theta_1-\theta_2\right)\nonumber                \\
       & \qquad =m_2 l_1 l_2 \dot{\theta}_1 \dot{\theta}_2 \sin \left(\theta_1-\theta_2\right)-m_2 g l_2 \sin \theta_2
\end{aligned}$$ After some re-arranging we get: $$\begin{aligned}
       & \ddot{\theta}_1+\frac{m_2}{m_1+m_2}\frac{ l_2}{l_1 } \cos \left(\theta_1-\theta_2\right)\ddot{\theta}_2  = \frac{-m_2 l_1 l_2 \dot{\theta}_2^2 \sin \left(\theta_1-\theta_2\right)-\left(m_1+m_2\right) g l_1 \sin \theta_1 }{(m_1+m_2)l_1^2} \\
       & \frac{l_1}{l_2}\cos\left(\theta_1-\theta_2\right)\ddot\theta_1+\ddot{\theta}_2=  \frac{m_2 l_1 l_2 \dot{\theta}_1^2 \sin \left(\theta_1-\theta_2\right)-m_2 g l_2 \sin \theta_2}{m_2l_2^2}
\end{aligned}$$ We introduce the notations: $$\begin{aligned}
       & c_{12}=\frac{m_2}{m_1+m_2}\frac{ l_2}{l_1 } \cos \left(\theta_1-\theta_2\right), \quad c_{21}=\frac{l_1}{l_2} \cos \left(\theta_1-\theta_2\right),\nonumber                                                                                        \\
       & C_1=-\frac{l_2}{l_1}\left(\frac{m_2}{m_1+m_2}\right) \dot{\theta}_2^2 \sin \left(\theta_1-\theta_2\right)-\frac{g}{l_1} \sin \theta_1  ,\quad C_2=\frac{l_1}{l_2} \dot{\theta}_1^2 \sin \left(\theta_1-\theta_2\right)-\frac{g}{l_2} \sin \theta_2
\end{aligned}$$ With these, the above system can be written as:

$
        \ddot{\theta}_1+c_{12}\ddot{\theta}_2=C_1  $ 
    
        $  c_{21}\ddot{\theta}_1+\ddot{\theta}_2=C_2$

We can solve the above system for $\ddot{\theta}_1$ and
$\ddot{\theta}_2$ to get:

 $\ddot\theta_1 = \frac{C_1-c_{12} C_2}{1-c_{12}c_{21}}  $  and 

        $ \ddot\theta_2 =\frac{C_2-c_{21} C_1}{1-c_{12}c_{21}}$

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


3.  **Compute and Display Poincaré Section:**
    Calculates and plots a Poincaré section, providing insights into the system's long-term behavior. The section is taken at a constant value of a chosen observable, as defined by `i_section` in `main.py`'s `poincare_animation()` function. The displayed coordinates are defined by `i1` and `i2`. Also the fractal dimension of the Poincare section is calculated. 
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
    Initial conditions are determined by the total energy `DeltaE`. The `find_initial_conditions(DeltaE)` function sets `q1_0`, `q2_0`, `omega1_0`, `omega2_0` based on this energy level, handling different initial configurations. Only one initial condition compatible to a given Delta E is used.

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
│   └── animation.py       # creates animations
│   └── fractal.py         # computes the fractal dimension
└── .gitignore        # Git ignore file
```

# Contributing

Contributions are welcome! If you have suggestions for improvements, bug fixes, or new features, please open an issue or submit a pull request.

## License

This project is open-source and available under the [MIT License](LICENSE.md).
