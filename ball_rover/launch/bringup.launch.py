import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import (
    IncludeLaunchDescription,
    ExecuteProcess,
    TimerAction
)
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node


def generate_launch_description():

    pkg_share = get_package_share_directory("ball_rover")

    map_file = os.path.join(
        pkg_share,
        "maps",
        "map_save.yaml"
    )

    params_file = os.path.join(
        pkg_share,
        "config",
        "nav2_params.yaml"
    )

    # Gazebo + Robot
    sim_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                pkg_share,
                "launch",
                "launch_sim.launch.py"
            )
        )
    )

    # Localization
    localization_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory("nav2_bringup"),
                "launch",
                "localization_launch.py"
            )
        ),
        launch_arguments={
            "map": map_file,
            "use_sim_time": "true",
            "params_file": params_file,
        }.items()
    )

    # Navigation2
    nav2_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                pkg_share,
                "launch",
                "nav2.launch.py"
            )
        )
    )

    # Ball Tracker
    tracker_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory("ball_tracker"),
                "launch",
                "ball_tracker.launch.py"
            )
        ),
        launch_arguments={
            "params_file": os.path.join(
                pkg_share,
                "config",
                "ball_tracker_params_sim.yaml"
            ),
            "image_topic": "/camera/image_raw",
            "cmd_vel_topic": "/cmd_vel_tracker",
            "enable_3d_tracker": "true"
        }.items()
    )

    # cmd_vel selector
    cmd_vel_selector_node = Node(
        package="ball_rover",
        executable="cmd_vel_selector.py",
        name="cmd_vel_selector",
        output="screen",
        remappings=[
            ("/cmd_vel", "/cmd_vel_nav"),
        ],
    )

    # Camera / RViz
    rviz_camera = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                pkg_share,
                "launch",
                "camera.launch.py"
            )
        )
    )

    

    # Initial Pose
    initial_pose = TimerAction(
        period=8.0,
        actions=[
            ExecuteProcess(
                cmd=[
                    "ros2",
                    "topic",
                    "pub",
                    "/initialpose",
                    "geometry_msgs/msg/PoseWithCovarianceStamped",
                    "{header: {frame_id: 'map'}, pose: {pose: {position: {x: 0.0, y: 0.0, z: 0.0}, orientation: {w: 1.0}}}}",
                    "--once"
                ],
                output="screen"
            )
        ]
    )

    # Ball Tracker State Machine
    state_machine_process = TimerAction(
        period=15.0,
        actions=[
            ExecuteProcess(
                cmd=[
                    "ros2",
                    "run",
                    "ball_tracker",
                    "state_machine"
                ],
                output="screen"
            )
        ]
    )

    return LaunchDescription([
        sim_launch,
        localization_launch,
        nav2_launch,
        tracker_launch,
        cmd_vel_selector_node,
        rviz_camera,
        initial_pose,
        state_machine_process
    ])