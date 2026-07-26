import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import SetRemap
def generate_launch_description():
    nav2_bringup_dir = get_package_share_directory("nav2_bringup")
    params_file = os.path.join(
        get_package_share_directory("ball_rover"),
        "config",
        "nav2_params.yaml"
    )
    navigation = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                nav2_bringup_dir,
                "launch",
                "navigation_launch.py"
            )
        ),
        launch_arguments={
            "use_sim_time": "true",
            "params_file": params_file,
        }.items(),
    )
    return LaunchDescription([
        # CHANGED: Nav2's cmd_vel now goes to an INTERMEDIATE topic
        # (/cmd_vel_nav) instead of straight to diff_drive_controller.
        # cmd_vel_selector.py (launched separately) decides, based on
        # /robot_state, whether this or follow_ball's command actually
        # reaches /diff_cont/cmd_vel_unstamped.
        SetRemap(
            src="/cmd_vel",
            dst="/cmd_vel_nav",
        ),
        navigation,
    ])