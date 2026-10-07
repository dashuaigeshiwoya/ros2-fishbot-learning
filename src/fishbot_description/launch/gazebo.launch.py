import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node


def generate_launch_description():
    fishbot_share = get_package_share_directory(
        'fishbot_description'
    )

    urdf_path = os.path.join(
        fishbot_share,
        'urdf',
        'fishbot_base.urdf',
    )

    world_path = os.path.join(
        fishbot_share,
        'world',
        'learning.world',
    )

    # 读取 URDF，供 robot_state_publisher 使用
    with open(urdf_path, 'r', encoding='utf-8') as urdf_file:
        robot_description = urdf_file.read()

    gazebo_share = get_package_share_directory('gazebo_ros')

    gazebo_launch_path = os.path.join(
        gazebo_share,
        'launch',
        'gazebo.launch.py',
    )

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(gazebo_launch_path),
        launch_arguments={
            'world': world_path,
        }.items(),
    )

    spawn_robot = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=[
            '-entity', 'fishbot_1',
            '-file', urdf_path,
            '-x', '0.0',
            '-y', '0.0',
            '-z', '0.20',
        ],
        output='screen',
    )

    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{
            'robot_description': robot_description,
            'use_sim_time': True,
        }],
        output='screen',
    )

    rviz = Node(
        package='rviz2',
        executable='rviz2',
        parameters=[{
            'use_sim_time': True,
        }],
        output='screen',
    )

    return LaunchDescription([
        gazebo,
        robot_state_publisher,
        spawn_robot,
        rviz,
    ])