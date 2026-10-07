import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource


def generate_launch_description():

    # 找到我们自己的导航包
    fishbot_share = get_package_share_directory(
        'fishbot_navigation2'
    )

    # 找到 Nav2 官方包
    nav2_share = get_package_share_directory(
        'nav2_bringup'
    )

    # 保存好的地图
    map_file = os.path.join(
        fishbot_share,
        'maps',
        'fishbot_map.yaml'
    )

    # Nav2 参数文件
    params_file = os.path.join(
        fishbot_share,
        'config',
        'fishbot_nav2.yaml'
    )

    # 调用 Nav2 官方 bringup_launch.py
    nav2 = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                nav2_share,
                'launch',
                'bringup_launch.py'
            )
        ),

        launch_arguments={
            'slam': 'False',
            'map': map_file,
            'params_file': params_file,
            'use_sim_time': 'True',
            'autostart': 'True',
            'use_composition': 'False',
        }.items()
    )

    return LaunchDescription([
        nav2
    ])