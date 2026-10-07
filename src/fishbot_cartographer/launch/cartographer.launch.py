import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    package_share = get_package_share_directory(
        'fishbot_cartographer'
    )

    configuration_directory = os.path.join(
        package_share,
        'config'
    )

    cartographer_node = Node(
        package='cartographer_ros',
        executable='cartographer_node',
        name='cartographer_node',
        output='screen',
        parameters=[
            {
                'use_sim_time': True
            }
        ],
        arguments=[
            '-configuration_directory',
            configuration_directory,
            '-configuration_basename',
            'fishbot_2d.lua'
        ],
        remappings=[
            ('scan', '/scan'),
            ('odom', '/odom')
        ]
    )

    occupancy_grid_node = Node(
        package='cartographer_ros',
        executable='cartographer_occupancy_grid_node',
        name='cartographer_occupancy_grid_node',
        output='screen',
        parameters=[
            {
                'use_sim_time': True
            }
        ],
        arguments=[
            '-resolution',
            '0.05',
            '-publish_period_sec',
            '1.0'
        ]
    )

    return LaunchDescription([
        cartographer_node,
        occupancy_grid_node
    ])