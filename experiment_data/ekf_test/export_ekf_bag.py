import os
import sys
import csv

import rosbag2_py

from rclpy.serialization import deserialize_message
from rosidl_runtime_py.utilities import get_message


if len(sys.argv) != 2:
    print("Usage:")
    print("python3 export_ekf_bag.py <bag_directory>")
    sys.exit(1)


bag_path = os.path.abspath(sys.argv[1])

output_dir = os.path.join(
    os.path.dirname(bag_path),
    os.path.basename(bag_path) + "_csv"
)

os.makedirs(output_dir, exist_ok=True)


reader = rosbag2_py.SequentialReader()

storage_options = rosbag2_py.StorageOptions(
    uri=bag_path,
    storage_id="sqlite3"
)

converter_options = rosbag2_py.ConverterOptions(
    input_serialization_format="cdr",
    output_serialization_format="cdr"
)

reader.open(
    storage_options,
    converter_options
)


topic_types = {
    topic.name: topic.type
    for topic in reader.get_all_topics_and_types()
}


odom_file = open(
    os.path.join(output_dir, "odom_raw.csv"),
    "w",
    newline=""
)

imu_file = open(
    os.path.join(output_dir, "imu_raw.csv"),
    "w",
    newline=""
)

filtered_file = open(
    os.path.join(output_dir, "odometry_filtered.csv"),
    "w",
    newline=""
)


odom_writer = csv.writer(odom_file)
imu_writer = csv.writer(imu_file)
filtered_writer = csv.writer(filtered_file)


odom_writer.writerow([
    "time_s",
    "position_x",
    "position_y",
    "linear_x",
    "angular_z"
])

imu_writer.writerow([
    "time_s",
    "angular_velocity_z",
    "linear_acceleration_x",
    "linear_acceleration_y"
])

filtered_writer.writerow([
    "time_s",
    "position_x",
    "position_y",
    "linear_x",
    "angular_z"
])


t0 = None


while reader.has_next():

    topic, data, timestamp = reader.read_next()

    if topic not in [
        "/odom",
        "/imu",
        "/odometry/filtered"
    ]:
        continue

    if t0 is None:
        t0 = timestamp

    time_s = (timestamp - t0) / 1e9

    msg_type = get_message(
        topic_types[topic]
    )

    msg = deserialize_message(
        data,
        msg_type
    )

    if topic == "/odom":

        odom_writer.writerow([
            time_s,
            msg.pose.pose.position.x,
            msg.pose.pose.position.y,
            msg.twist.twist.linear.x,
            msg.twist.twist.angular.z
        ])

    elif topic == "/imu":

        imu_writer.writerow([
            time_s,
            msg.angular_velocity.z,
            msg.linear_acceleration.x,
            msg.linear_acceleration.y
        ])

    elif topic == "/odometry/filtered":

        filtered_writer.writerow([
            time_s,
            msg.pose.pose.position.x,
            msg.pose.pose.position.y,
            msg.twist.twist.linear.x,
            msg.twist.twist.angular.z
        ])


odom_file.close()
imu_file.close()
filtered_file.close()


print("Export finished.")
print("CSV directory:")
print(output_dir)


