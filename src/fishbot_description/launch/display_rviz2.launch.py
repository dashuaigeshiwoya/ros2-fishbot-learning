import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    # 找到安装后的功能包资源目录
    package_share = get_package_share_directory(
        'fishbot_description'
    )

    # 找到要显示的模型文件
    urdf_path = os.path.join(
        package_share,
        'urdf',
        'fishbot_base.urdf',
    )

    # 读取模型文件内容
    with open(urdf_path, 'r', encoding='utf-8') as urdf_file:
        robot_description = urdf_file.read()

    # 根据模型和关节角度，发布部件的坐标关系
    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[
            {'robot_description': robot_description},
        ],
        output='screen',
    )

    # 提供关节角度，并打开滑块调节窗口
    joint_state_publisher_gui_node = Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui',
        arguments=[urdf_path],
        output='screen',
    )

    # 打开模型观察窗口
    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        output='screen',
    )

    return LaunchDescription([
        robot_state_publisher_node,
        joint_state_publisher_gui_node,
        rviz_node,
    ])