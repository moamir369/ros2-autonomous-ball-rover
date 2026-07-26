# Copyright 2026 [Muhammet Emir Hallek]
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


#!/usr/bin/env python3
import math
import yaml

import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from rclpy.duration import Duration

from std_msgs.msg import String
from geometry_msgs.msg import Point, PoseStamped
from nav2_msgs.action import NavigateToPose


class State:
    PATROL = "PATROL"
    TRACKING = "TRACKING"


def yaw_to_quaternion(yaw: float):
    return (0.0, 0.0, math.sin(yaw / 2.0), math.cos(yaw / 2.0))


class BallTrackerStateMachine(Node):
    def __init__(self):
        super().__init__('ball_tracker_state_machine')

        self.declare_parameter('ball_detected_topic', '/detected_ball')
        self.declare_parameter('state_topic', '/robot_state')
        self.declare_parameter('ball_lost_timeout', 2.0)  # seconds
        self.declare_parameter('waypoints_file', '')       # optional yaml path
        self.declare_parameter(
            'waypoints',
                [0.0, 0.0, 0.0,
                2.0, 0.0, 0.0,
                2.0, 2.0, 1.57,
                0.0, 2.0, 3.14]
        )  

        ball_topic = self.get_parameter('ball_detected_topic').value
        state_topic = self.get_parameter('state_topic').value
        self.ball_lost_timeout = float(self.get_parameter('ball_lost_timeout').value)

        self.waypoints = self._load_waypoints()
        self.current_wp_index = 0

        self.state = State.PATROL
        self.last_ball_seen_time = None

        self.state_pub = self.create_publisher(String, state_topic, 10)
        self.ball_sub = self.create_subscription(
            Point, ball_topic, self.ball_callback, 10
        )

        self.nav_client = ActionClient(self, NavigateToPose, 'navigate_to_pose')
        self._current_goal_handle = None
        self._nav_active = False

        self.create_timer(0.2, self.control_loop)   
        self.create_timer(0.5, self.publish_state)

        self.get_logger().info(
            f'State machine started with {len(self.waypoints)} waypoints. '
            f'ball_topic={ball_topic}, ball_lost_timeout={self.ball_lost_timeout}s'
        )

        # Kick off patrol
        self._send_next_waypoint()

    def _load_waypoints(self):
        path = self.get_parameter('waypoints_file').value
        if path:
            with open(path, 'r') as f:
                data = yaml.safe_load(f)
            return [(wp['x'], wp['y'], wp.get('yaw', 0.0)) for wp in data['waypoints']]

        flat = self.get_parameter('waypoints').value
        return [(flat[i], flat[i + 1], flat[i + 2]) for i in range(0, len(flat), 3)]

    def ball_callback(self, msg: Point):
        self.last_ball_seen_time = self.get_clock().now()
        if self.state == State.PATROL:
            self.get_logger().info('Ball detected -> switching to TRACKING')
            self._enter_tracking()

    def control_loop(self):
        if self.state == State.TRACKING:
            if self.last_ball_seen_time is None:
                return
            elapsed = (self.get_clock().now() - self.last_ball_seen_time).nanoseconds / 1e9
            if elapsed > self.ball_lost_timeout:
                self.get_logger().info('Ball lost -> switching back to PATROL')
                self._enter_patrol()

    def _enter_tracking(self):
        self.state = State.TRACKING
        self._cancel_current_goal()

    def _enter_patrol(self):
        self.state = State.PATROL
        self._send_next_waypoint()

    def publish_state(self):
        msg = String()
        msg.data = self.state
        self.state_pub.publish(msg)

    def _send_next_waypoint(self):
        if self.state != State.PATROL:
            return
        if not self.nav_client.wait_for_server(timeout_sec=2.0):
            self.get_logger().warn('Nav2 action server not available yet')
            return

        x, y, yaw = self.waypoints[self.current_wp_index]
        goal_msg = NavigateToPose.Goal()
        pose = PoseStamped()
        pose.header.frame_id = 'map'
        pose.header.stamp = self.get_clock().now().to_msg()
        pose.pose.position.x = x
        pose.pose.position.y = y
        qx, qy, qz, qw = yaw_to_quaternion(yaw)
        pose.pose.orientation.x = qx
        pose.pose.orientation.y = qy
        pose.pose.orientation.z = qz
        pose.pose.orientation.w = qw
        goal_msg.pose = pose

        self.get_logger().info(f'Sending waypoint #{self.current_wp_index}: ({x}, {y}, {yaw})')
        self._nav_active = True
        send_goal_future = self.nav_client.send_goal_async(goal_msg)
        send_goal_future.add_done_callback(self._goal_response_callback)

    def _goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().warn('Nav2 goal rejected')
            self._nav_active = False
            return
        self._current_goal_handle = goal_handle
        result_future = goal_handle.get_result_async()
        result_future.add_done_callback(self._goal_result_callback)

    def _goal_result_callback(self, future):
        self._nav_active = False
        if self.state != State.PATROL:
            return 
        
        self.current_wp_index = (self.current_wp_index + 1) % len(self.waypoints)
        self._send_next_waypoint()

    def _cancel_current_goal(self):
        if self._current_goal_handle is not None and self._nav_active:
            self.get_logger().info('Cancelling current Nav2 goal')
            cancel_future = self._current_goal_handle.cancel_goal_async()
            cancel_future.add_done_callback(lambda f: None)
        self._nav_active = False


def main(args=None):
    rclpy.init(args=args)
    node = BallTrackerStateMachine()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()