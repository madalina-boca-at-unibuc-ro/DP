import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from tqdm import tqdm
import time

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
    sol = solve_ivp(
        lagrange_equations,
        t_span,
        y0,
        t_eval=t_eval,
        method="DOP853",
        rtol=1e-10,
        atol=1e-10,
    )
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


def normalize_vector_angle(angle):
    normalized_angle = np.fmod(angle, 2 * np.pi)
    normalized_angle = np.where(
        normalized_angle > np.pi, normalized_angle - 2 * np.pi, normalized_angle
    )
    normalized_angle = np.where(
        normalized_angle < -np.pi, normalized_angle + 2 * np.pi, normalized_angle
    )
    return normalized_angle


def normalize_angle(angle):
    normalized_angle = np.fmod(angle, 2 * np.pi)
    normalized_angle = (
        normalized_angle - 2 * np.pi if normalized_angle > np.pi else normalized_angle
    )
    normalized_angle = (
        normalized_angle + 2 * np.pi if normalized_angle < -np.pi else normalized_angle
    )
    return normalized_angle


def compute_observables(y):

    q1, q2, omega1, omega2 = y
    p1 = (m1 + m2) * L1 * L1 * omega1 + m2 * L1 * L2 * omega2 * np.cos(q1 - q2)
    p2 = m2 * L2 * L2 * omega2 + m2 * L1 * L2 * omega1 * np.cos(q1 - q2)

    T = (
        m1 * L1 * L1 * omega1 * omega1 / 2
        + m2
        * (
            L1 * L1 * omega1 * omega1
            + L2 * L2 * omega2 * omega2
            + 2 * L1 * L2 * omega1 * omega2 * np.cos(q1 - q2)
        )
        / 2
    )
    V = -(m1 + m2) * g * L1 * np.cos(q1) - m2 * L2 * g * np.cos(q2)
    omega1 = normalize_angle(omega1)
    omega2 = normalize_angle(omega2)

    return [q1, q2, omega1, omega2, p1, p2, T + V]


def interpolate_observables(observable_old, observable_new, i_section):
    a_1 = observable_old[i_section]
    a_2 = observable_new[i_section]

    if a_1 * a_2 > 0:
        print("The section is not crossed")
        exit()
    else:
        observable = np.zeros(len(observable_old))
        slope = -a_1 / (a_2 - a_1)
        for i in range(len(observable_old)):
            b_1 = observable_old[i]
            b_2 = observable_new[i]
            res = slope * (b_2 - b_1) + b_1
            if i == 0 or i == 1:
                res = normalize_angle(res)
            observable[i] = res
        return observable


labels = ["q1", "q2", "omega1", "omega2", "p1", "p2"]


def trajectory_animation():
    # index  of the observable to plot
    i1 = 0
    i2 = 1
    """
    index = 0  - q1 (normalized)
    index = 1  - q2 (normalized)
    index = 2  - omega1 (normalized)
    index = 3  - omega2 (normalized)
    index = 4  - p1 (normalized)
    index = 5  - p2 (normalized)
    """

    DeltaE = 25
    y0 = find_initial_conditions(DeltaE)

    t_span = (0, 100)
    t_eval = np.linspace(*t_span, 10000)

    print("Double Pendulum trajectory")
    sol = solve_ivp(
        lagrange_equations,
        t_span,
        y0,
        t_eval=t_eval,
        method="DOP853",
        rtol=1e-10,
        atol=1e-10,
    )

    observables = compute_observables(sol.y)

    # normalize the observables
    observables[0] = normalize_vector_angle(observables[0])
    observables[1] = normalize_vector_angle(observables[1])
    for i in range(2, 6):
        den = np.max(np.abs(observables[i]))
        if den != 0:
            observables[i] = observables[i] / den

    # Animation
    fig, ax = plt.subplots()
    ax.set_aspect("equal")
    ax.set_xlim(-1.2, 1.2)
    ax.set_ylim(-1.2, 1.2)
    ax.set_xlabel(labels[i1])
    ax.set_ylabel(labels[i2])
    (trail,) = ax.plot([], [], "r-", alpha=0.4, lw=1)

    q1_trail, q2_trail = [], []

    def init():
        trail.set_data([], [])
        return trail

    def update(frame):
        q1_trail.append(observables[i1][frame])
        q2_trail.append(observables[i2][frame])
        trail.set_data(q1_trail, q2_trail)
        return trail

    ani = FuncAnimation(
        fig,
        update,
        frames=len(t_eval),
        init_func=init,
        blit=False,
        interval=2,
    )
    plt.title("Double Pendulum trajectory (" + labels[i1] + ", " + labels[i2] + ")")


    plt.show()


def poincare_animation():

    print("Double Pendulum poincare section")

    # index  of the observable to plot
    i1 = 0
    i2 = 1

    # index of the section of the trajectory to plot
    i_section = 4

    """
    index = 0  - q1 (normalized)
    index = 1  - q2 (normalized)
    index = 2  - omega1 (normalized)
    index = 3  - omega2 (normalized)
    index = 4  - p1 (normalized)
    index = 5  - p2 (normalized)
    """

    # Np : The number of points in the Poincare section
    Np = 100000

    DeltaE = 25
    y0 = find_initial_conditions(DeltaE)
    observable_old = compute_observables(y0)

    t_0 = 0
    dt = 0.01
    print(f"Calculating {Np} points in the Poincare section")

    Observables = np.zeros((7, Np))
    N_filled_points = 0

    pbar = tqdm(total=Np)
    while N_filled_points < Np:
        sol = solve_ivp(
            lagrange_equations,
            (t_0, t_0 + dt),
            y0,
            method="DOP853",
            rtol=1e-10,
            atol=1e-10,
        )
        y = sol.y[:, -1]
        observable_new = compute_observables(y)
        if observable_new[i_section] * observable_old[i_section] < 0:
            Observables[:, N_filled_points] = interpolate_observables(
                observable_old, observable_new, i_section
            )
            N_filled_points += 1
            pbar.update(1)
        observable_old = observable_new
        t_0 += dt
        y0 = y
    pbar.close()

    for i in range(0, 2):
        Observables[i] /= np.pi  # normalize the observables
    for i in range(2, 5):
        den = np.max(np.abs(Observables[i]))
        if den != 0:
            Observables[i] = Observables[i] / den

    fig, ax = plt.subplots()
    ax.set_aspect("equal")
    ax.set_xlim(-1.2, 1.2)
    ax.set_ylim(-1.2, 1.2)
    ax.set_xlabel(labels[i1])
    ax.set_ylabel(labels[i2])
    ax.set_title("Double Pendulum Poincare section ("
            + labels[i1]
            + ", "
            + labels[i2]
            + ")\n"
            + "at zero " + labels[i_section]
            + " ; "
            + str(len(Observables[0])) + " points")
    ax.grid(True)
    ax.plot(Observables[i1], Observables[i2], ",", color="r", alpha=0.2, markersize=0.01)

    plt.savefig("poincare_section.png", dpi = 300)
    plt.show()
    plt.close()

    # Animation
    fig, ax = plt.subplots()
    ax.set_aspect("equal")
    ax.set_xlim(-1.2, 1.2)
    ax.set_ylim(-1.2, 1.2)
    ax.set_xlabel(labels[i1])
    ax.set_ylabel(labels[i2])
    (trail,) = ax.plot([], [], ",", color="r", alpha=0.2, markersize=0.01)

    q1_trail, q2_trail = [], []
    animation_title = ax.set_title("")

    def init():
        trail.set_data([], [])
        animation_title.set_text("")
        return trail

    def update(frame):
        for i in range(0, 10):
            q1_trail.append(Observables[i1][frame * 10 + i])
            q2_trail.append(Observables[i2][frame * 10 + i])
        trail.set_data(q1_trail, q2_trail)
        animation_title.set_text(
            "Double Pendulum Poincare section ("
            + labels[i1]
            + ", "
            + labels[i2]
            + ")\nat zero "
            + labels[i_section]
            + " frame "
            + str(frame * 10)
            + "/"
            + str(len(Observables[0]))
        )

        return trail

    ani = FuncAnimation(
        fig,
        update,
        frames=len(Observables[0])//10,
        init_func=init,
        blit=False,
        interval=2,
    )

    plt.show()
