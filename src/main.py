import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Constants
g = 10  # m/s^2 (for simplicity g = 10)
m1, m2 = 1.0, 1.0  # kg
L1, L2 = 1.0, 1.0  # m


# Lagrange equations (the differential equations equivalent to the Newton's equations)
def lagrange_equations(t, y):
    q1, q2, omega1, omega2 = y

    q1_dot = omega1
    q2_dot = omega2

    alpha1 = L2 / L1 * m2 / (m1 + m2) * np.cos(q1 - q2)
    alpha2 = L1 / L2 * np.cos(q1 - q2)
    f1 = -L2 / L1 * m2 / (m1 + m2) * omega2 * omega2 * np.sin(
        q1 - q2
    ) - g / L1 * np.sin(q1)
    f2 = L1 / L2 * omega1 * omega1 * np.sin(q1 - q2) - g / L2 * np.sin(q2)

    omega1_dot = (f1 - alpha1 * f2) / (1 - alpha1 * alpha2)
    omega2_dot = (f2 - alpha2 * f1) / (1 - alpha1 * alpha2)

    return [q1_dot, q2_dot, omega1_dot, omega2_dot]


# Initial conditions are fixed in terms of the total energy


def find_initial_conditions(DeltaE):

    if DeltaE < 0:
        print("DeltaE must be positive")
        return [0.0, 0.0, 0.0, 0.0]
    elif DeltaE < 2 * m2 * g * L2:
        print("The lower pendulum is tilted at the initial moment")
        q2_0 = np.acos(1 - DeltaE / (m2 * g * L2))
        return [0.0, q2_0, 0.0, 0.0]
    elif DeltaE < 2 * (m1 + m2) * g * L1 + 2 * m2 * g * L2:
        print(
            "The lower pendulum is in the vertical position (q2_0=pi); the upper pendulum is tilted at the initial moment"
        )
        q2_0 = np.pi
        q1_0 = np.acos((2 * m2 * g * L2 - DeltaE) / (2 * (m1 + m2) * g * L1))
        return [q1_0, q2_0, 0.0, 0.0]
    else:
        print(
            "Both pendulums are in the vertical position (q1_0=q2_0=pi) and the pendulum 2 has an angular velocity"
        )
        q1_0 = np.pi
        q2_0 = np.pi
        omega2_0 = np.sqrt(
            2 * (DeltaE - (2 * (m1 + m2) * g * L1 + 2 * m2 * g * L2)) / (m2 * L2**2)
        )
        return [q1_0, q2_0, 0.0, omega2_0]


def pendulum_animation():

    DeltaE = 75
    y0 = find_initial_conditions(DeltaE)

    t_span = (0, 100)
    t_eval = np.linspace(*t_span, 10000)

    print("Double Pendulum Animation")
    sol = solve_ivp(lagrange_equations, t_span, y0, t_eval=t_eval, method="DOP853")
    q1, q2 = sol.y[0], sol.y[1]

    # Convert to Cartesian coordinates
    x1 = L1 * np.sin(q1)
    y1 = -L1 * np.cos(q1)
    x2 = x1 + L2 * np.sin(q2)
    y2 = y1 - L2 * np.cos(q2)

    # Animation
    fig, ax = plt.subplots()
    ax.set_aspect("equal")
    ax.set_xlim(-2.2, 2.2)
    ax.set_ylim(-2.2, 2.2)
    (line,) = ax.plot([], [], "o-", lw=2)
    (trail,) = ax.plot([], [], "r-", alpha=0.4, lw=1)

    x2_trail, y2_trail = [], []

    def init():
        line.set_data([], [])
        trail.set_data([], [])
        return line, trail

    def update(frame):
        x = [0, x1[frame], x2[frame]]
        y = [0, y1[frame], y2[frame]]
        line.set_data(x, y)
        x2_trail.append(x2[frame])
        y2_trail.append(y2[frame])
        trail.set_data(x2_trail, y2_trail)
        return line, trail

    ani = FuncAnimation(
        fig,
        update,
        frames=len(t_eval),
        init_func=init,
        blit=False,
        interval=20,
    )
    plt.title("Double Pendulum Animation (Lagrange equations)")
    plt.show()


def trajectory_animation():

    DeltaE = 15
    y0 = find_initial_conditions(DeltaE)

    t_span = (0, 100)
    t_eval = np.linspace(*t_span, 10000)

    def normalize_angle(angle):
        normalized_angle = np.fmod(angle, 2 * np.pi)
        normalized_angle = np.where(
            normalized_angle > np.pi, normalized_angle - 2 * np.pi, normalized_angle
        )
        return normalized_angle / np.pi

    print("Double Pendulum trajectory")
    sol = solve_ivp(lagrange_equations, t_span, y0, t_eval=t_eval, method="DOP853")
    q1, q2 = normalize_angle(sol.y[0]), normalize_angle(sol.y[1])

    # Animation
    fig, ax = plt.subplots()
    ax.set_aspect("equal")
    ax.set_xlim(-1.2, 1.2)
    ax.set_ylim(-1.2, 1.2)
    ax.set_xlabel("q1 (pi)")
    ax.set_ylabel("q2 (pi)")
    (trail,) = ax.plot([], [], "r-", alpha=0.4, lw=1)

    q1_trail, q2_trail = [], []

    def init():
        trail.set_data([], [])
        return trail

    def update(frame):
        q1_trail.append(q1[frame])
        q2_trail.append(q2[frame])
        trail.set_data(q1_trail, q2_trail)
        return trail

    ani = FuncAnimation(
        fig,
        update,
        frames=len(t_eval),
        init_func=init,
        blit=False,
        interval=20,
    )
    plt.title("Double Pendulum trajectory (q1, q2)")
    plt.show()
