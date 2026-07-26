#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_msgs.msg import String
import time

class CmdVelSelector(Node):

    def __init__(self):

        super().__init__("cmd_vel_selector")

        self.nav_msg = Twist()
        self.tracker_msg = Twist()

        self.last_tracker_time = 0.0

        self.current_state = "PATROL"
        self.create_subscription(
            String,
            "/robot_state",
            self.state_callback,
            10
        )

        # Nav2
        self.create_subscription(
            Twist,
            "/cmd_vel",
            self.nav_callback,
            10
        )

        # Ball Tracker
        self.create_subscription(
            Twist,
            "/cmd_vel_tracker",
            self.tracker_callback,
            10
        )

        # Robot
        self.publisher = self.create_publisher(
            Twist,
            "/diff_cont/cmd_vel_unstamped",
            10
        )

        self.timer = self.create_timer(
            0.05,
            self.publish_cmd
        )

    def state_callback(self, msg):

        self.current_state = msg.data

    def nav_callback(self, msg):

        self.nav_msg = msg

    def tracker_callback(self, msg):

        self.tracker_msg = msg
        self.last_tracker_time = time.time()

    def publish_cmd(self):

        now = time.time()
        tracker_is_fresh = (now - self.last_tracker_time) < 0.5

        if self.current_state == "TRACKING":
            if tracker_is_fresh:
                self.publisher.publish(self.tracker_msg)
            else:
                self.publisher.publish(Twist())
        else:
            self.publisher.publish(self.nav_msg)


def main(args=None):

    rclpy.init(args=args)

    node = CmdVelSelector()

    rclpy.spin(node)

    node.destroy_node()

    rclpy.shutdown()


if __name__ == "__main__":
    main()