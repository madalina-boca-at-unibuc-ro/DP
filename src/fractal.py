import matplotlib.pyplot as plt
import numpy as np
import os


def calculate_occupied_boxes(points=None, i1=0, i2=1, r=2, bbox=(-1, 1, -1, 1)):
    """
    Calculates the number of boxes of size 'r' that contain at least one point.
    bbox: (min_x, max_x, min_y, max_y)
    """

    if points is None:
        return 0

    min_x, max_x, min_y, max_y = bbox

    # Handle cases where the bounding box might be a single point or line
    # Add a small epsilon to avoid division by zero if width/height is zero
    effective_width = max_x - min_x
    effective_height = max_y - min_y

    if effective_width == 0:
        effective_width = r  # Treat as one box wide if points are on a vertical line
    if effective_height == 0:
        effective_height = r  # Treat as one box high if points are on a horizontal line

    num_boxes_x = int(np.ceil(effective_width / r))
    num_boxes_y = int(np.ceil(effective_height / r))

    occupied_boxes = set()

    for p_x, p_y in zip(points[i1], points[i2]):
        box_x = int(np.floor((p_x - min_x) / r))
        box_y = int(np.floor((p_y - min_y) / r))

        # Clamp indices to prevent going out of bounds due to floating point inaccuracies
        box_x = min(box_x, num_boxes_x - 1)
        box_y = min(box_y, num_boxes_y - 1)

        occupied_boxes.add((box_x, box_y))

    return len(occupied_boxes)


def calculate_fractal_dimension(
    points=None, i1=0, i2=1, bbox=(-1, 1, -1, 1), num_boxes=6, folder_name="."
):

    # --- Setup Plot ---
    fig_viz, ax_viz = plt.subplots(figsize=(8, 8))
    ax_viz.set_aspect("equal", adjustable="box")
    ax_viz.set_title("Fractal Dimension: Box-Counting Method")
    ax_viz.set_xlabel("X-coordinate")
    ax_viz.set_ylabel("Y-coordinate")
    ax_viz.grid(True, linestyle="--", alpha=0.6)

    min_x, max_x, min_y, max_y = bbox
    # Calculate the range for both x and y
    x_range = max_x - min_x
    y_range = max_y - min_y
    # Use the larger range to ensure square aspect ratio
    max_range = max(x_range, y_range)
    if max_range == 0:
        max_range = 1.0  # Avoid division by zero

    # Set equal limits for both axes to ensure 1:1 aspect ratio
    padding = max_range * 0.1  # 10% padding
    center_x = (min_x + max_x) / 2
    center_y = (min_y + max_y) / 2
    half_range = max_range / 2 + padding

    ax_viz.set_xlim(center_x - half_range, center_x + half_range)
    ax_viz.set_ylim(center_y - half_range, center_y + half_range)

    # Calculate max dimension of the bounding box for box size scaling
    max_dim = max(max_x - min_x, max_y - min_y)
    if max_dim == 0:  # Handle case of single point
        max_dim = 1.0  # Arbitrary small value to allow box sizes to be calculated

    # Define a range of box sizes (r)
    box_sizes = [max_dim / (2 ** (i + 1)) for i in range(num_boxes)]
    if not box_sizes:  # Ensure at least one box size if max_dim was very small
        box_sizes = [1.0]

    # Initialize plot elements
    (point_plot,) = ax_viz.plot(
        points[i1],
        points[i2],
        ",",
        markersize=0.2,
        color="#4A5568",
        label="Points",
    )
    rect_patches = []  # To store the rectangles for occupied boxes
    current_info_text = ax_viz.text(
        0.02,
        0.98,
        "Box Size (r): 0.00\nOccupied Boxes (N(r)): 0",
        transform=ax_viz.transAxes,
        verticalalignment="top",
        fontsize=10,
        bbox=dict(boxstyle="round,pad=0.5", fc="white", ec="gray", lw=0.5, alpha=0.8),
    )

    # --- Save Each Frame as PNG and Data ---
    print("Saving individual frames and data...")

    # Create a list to store the data
    box_data = []

    for frame in range(len(box_sizes)):
        # Clear previous rectangles
        for rect in rect_patches:
            rect.remove()
        rect_patches.clear()

        # Get current box size
        r = box_sizes[frame]

        # Calculate occupied boxes
        occupied_count = calculate_occupied_boxes(
            points=points, i1=i1, i2=i2, r=r, bbox=bbox
        )

        # Store the data
        box_data.append((-np.log(r), np.log(occupied_count)))

        # Draw occupied boxes
        min_x, max_x, min_y, max_y = bbox
        num_boxes_x = int(np.ceil((max_x - min_x) / r)) if (max_x - min_x) > 0 else 1
        num_boxes_y = int(np.ceil((max_y - min_y) / r)) if (max_y - min_y) > 0 else 1

        occupied_set = set()
        for p_x, p_y in zip(points[i1], points[i2]):
            box_x = int(np.floor((p_x - min_x) / r))
            box_y = int(np.floor((p_y - min_y) / r))
            box_x = min(box_x, num_boxes_x - 1)
            box_y = min(box_y, num_boxes_y - 1)
            occupied_set.add((box_x, box_y))

        for bx, by in occupied_set:
            rect = plt.Rectangle(
                (min_x + bx * r, min_y + by * r),
                r,
                r,
                facecolor=(66 / 255, 153 / 255, 225 / 255, 0.5),
                edgecolor="#4299E1",
                linewidth=1.5,
            )
            ax_viz.add_patch(rect)
            rect_patches.append(rect)

        # Update info text
        current_info_text.set_text(
            f"Box Size (r): {r:.2f}\nOccupied Boxes (N(r)): {occupied_count}"
        )

        # Save the frame
        filename = os.path.join(folder_name, f"frame_{frame:02d}_r_{r:.2f}.png")
        plt.savefig(filename, dpi=150, bbox_inches="tight")

    plt.close(fig_viz)

    # Save the box counting data to a file
    data_filename = os.path.join(folder_name, "box_counting_data.txt")
    with open(data_filename, "w") as f:
        f.write("# Box Counting Data for Fractal Dimension Calculation\n")
        f.write("# Format: -log(box_size(r)) log(occupied_boxes(N(r)))\n")
        f.write("# Number of points: " + str(len(points[i1])) + "\n\n")

        for r, occupied_count in box_data:
            f.write(f"{r:.6f}\t{occupied_count}\n")

    print(f"All {len(box_sizes)} frames saved as PNG files!")
    print(f"Box counting data saved to: {data_filename}")

    # --- Perform Linear Regression for Fractal Dimension ---
    x_data = np.array([data[0] for data in box_data])
    y_data = np.array([data[1] for data in box_data])

    # Perform linear regression: polyfit returns coefficients [slope, intercept]
    # np.polyfit(x, y, degree)
    coefficients = np.polyfit(x_data, y_data, 1)
    fractal_dimension = coefficients[0]  # The slope is the fractal dimension
    intercept = coefficients[1]

    # Create a linear function from the coefficients
    fit_line = np.poly1d(coefficients)

    # --- Plotting the log-log fit ---
    fig_fit, ax_fit = plt.subplots(figsize=(8, 6))
    ax_fit.scatter(
        x_data, y_data, color="blue", label="Data Points: (log(1/r), log(N(r)))"
    )
    ax_fit.plot(
        x_data,
        fit_line(x_data),
        color="red",
        linestyle="--",
        label=f"Linear Fit (D = {fractal_dimension:.4f})",
    )

    ax_fit.set_title(
        f"Box-Counting Method: Log-Log Plot\nFractal Dimension D = {fractal_dimension:.4f}"
    )
    ax_fit.set_xlabel("log(1/r)")
    ax_fit.set_ylabel("log(N(r))")
    ax_fit.legend()
    ax_fit.grid(True, linestyle="--", alpha=0.6)

    # Save the log-log plot
    fit_filename = os.path.join(folder_name, "fractal_dimension_fit.png")
    plt.savefig(fit_filename, dpi=300, bbox_inches="tight")
    print(f"Fractal dimension fit plot saved to: {fit_filename}")
    plt.close(fig_fit)  # Close the fit figure
    print(f"Calculated Fractal Dimension (D): {fractal_dimension:.4f}")
