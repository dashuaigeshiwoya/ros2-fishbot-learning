import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node
def generate_launch_description():
    package_share = get_package_share_directory('fishbot_navigation2')

    config_file = os.path.join(
        package_share, 'config', 'ekf.yaml'
    )

    ekf_node = Node(
        package='robot_localization',
        executable='ekf_node',
        name='ekf_filter_node',
        output='screen',
        parameters=[config_file]
    )

    return LaunchDescription([ekf_node])