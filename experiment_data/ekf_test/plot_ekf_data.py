import csv
import os

import matplotlib.pyplot as plt


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CSV_DIR = os.path.join(
    BASE_DIR,
    "ekf_clean_03_csv"
)


def read_csv(filename):
    path = os.path.join(CSV_DIR, filename)

    with open(path, "r") as f:
        reader = csv.DictReader(f)
        return list(reader)


# ============================================================
# Read data
# ============================================================

odom = read_csv("odom_raw.csv")
imu = read_csv("imu_raw.csv")
filtered = read_csv("odometry_filtered.csv")


# ============================================================
# Raw odometry data
# ============================================================

odom_t = [
    float(row["time_s"])
    for row in odom
]

odom_x = [
    float(row["position_x"])
    for row in odom
]

odom_y = [
    float(row["position_y"])
    for row in odom
]

odom_vx = [
    float(row["linear_x"])
    for row in odom
]

odom_wz = [
    float(row["angular_z"])
    for row in odom
]


# ============================================================
# Raw IMU data
# ============================================================

imu_t = [
    float(row["time_s"])
    for row in imu
]

imu_wz = [
    float(row["angular_velocity_z"])
    for row in imu
]


# ============================================================
# EKF filtered data
# ============================================================

filtered_t = [
    float(row["time_s"])
    for row in filtered
]

filtered_x = [
    float(row["position_x"])
    for row in filtered
]

filtered_y = [
    float(row["position_y"])
    for row in filtered
]

filtered_vx = [
    float(row["linear_x"])
    for row in filtered
]

filtered_wz = [
    float(row["angular_z"])
    for row in filtered
]


# ============================================================
# Plot 1: Linear velocity
# Raw /odom vs EKF /odometry/filtered
# ============================================================

plt.figure(figsize=(10, 5))

plt.plot(
    odom_t,
    odom_vx,
    label="Raw odometry linear velocity"
)

plt.plot(
    filtered_t,
    filtered_vx,
    label="EKF filtered linear velocity"
)

plt.xlabel("Time (s)")
plt.ylabel("Linear velocity (m/s)")
plt.title("Raw Odometry vs EKF Filtered Linear Velocity")
plt.grid(True)
plt.legend()
plt.tight_layout()

plt.savefig(
    os.path.join(
        BASE_DIR,
        "01_linear_velocity_comparison.png"
    ),
    dpi=200
)

plt.close()


# ============================================================
# Plot 2: Angular velocity
# Raw /odom vs Raw /imu vs EKF result
# ============================================================

plt.figure(figsize=(10, 5))

plt.plot(
    odom_t,
    odom_wz,
    label="Raw odometry angular velocity"
)

plt.plot(
    imu_t,
    imu_wz,
    label="Raw IMU angular velocity"
)

plt.plot(
    filtered_t,
    filtered_wz,
    label="EKF filtered angular velocity"
)

plt.xlabel("Time (s)")
plt.ylabel("Angular velocity (rad/s)")
plt.title("Angular Velocity Sensor Fusion Comparison")
plt.grid(True)
plt.legend()
plt.tight_layout()

plt.savefig(
    os.path.join(
        BASE_DIR,
        "02_angular_velocity_comparison.png"
    ),
    dpi=200
)

plt.close()


# ============================================================
# Plot 3: XY trajectory
# Raw odometry vs EKF result
# ============================================================

plt.figure(figsize=(7, 7))

plt.plot(
    odom_x,
    odom_y,
    label="Raw odometry trajectory"
)

plt.plot(
    filtered_x,
    filtered_y,
    label="EKF filtered trajectory"
)

plt.xlabel("X position (m)")
plt.ylabel("Y position (m)")
plt.title("Robot Trajectory: Raw Odometry vs EKF")
plt.axis("equal")
plt.grid(True)
plt.legend()
plt.tight_layout()

plt.savefig(
    os.path.join(
        BASE_DIR,
        "03_trajectory_comparison.png"
    ),
    dpi=200
)

plt.close()


print("Finished.")
print("")
print("Generated:")
print("01_linear_velocity_comparison.png")
print("02_angular_velocity_comparison.png")
print("03_trajectory_comparison.png")

