import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription

from launch.launch_description_sources import PythonLaunchDescriptionSource

from launch_ros.actions import Node

def generate_launch_description():
    package_name ="ball_rover"

    pkg_share =get_package_share_directory(package_name)


    rviz_config = os.path.join(
        pkg_share,
        "rviz",
        "camera.rviz"
    )

    rviz_node = Node(
        package="rviz2",
        executable="rviz2",
        arguments=[
            "-d", rviz_config,
            "--ros-args",
            "-p", "use_sim_time:=true"
        ],
        output="screen"
    )


    return  LaunchDescription([
        rviz_node
    ])