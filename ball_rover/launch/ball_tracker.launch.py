import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource


def generate_launch_description():

    my_package_name = 'ball_rover'

    params_path = os.path.join(
        get_package_share_directory(my_package_name),
        'config',
        'ball_tracker_params_sim.yaml'
    )

    tracker_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory('ball_tracker'),
                'launch',
                'ball_tracker.launch.py'
            )
        ),
        launch_arguments={
            'params_file': params_path,
            'image_topic': '/camera/image_raw',
            'final_cmd_vel_topic': '/diff_cont/cmd_vel_unstamped',
            'enable_3d_tracker': 'true'
        }.items()
    )

    return LaunchDescription([
        tracker_launch,
    ])