#!/usr/bin/env python3

import sys
import tty
import termios
import select

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

class KeyboardTeleop(Node):
    def __init__(self):
        super().__init__('keyboard_teleop')
        
        self.declare_parameter('cmd_vel_topic', '/diff_cont/cmd_vel_unstamped')
        self.declare_parameter('linear_speed', 1.0)
        self.declare_parameter('angular_speed', 0.5)
        self.declare_parameter('publish_rate', 10.0) # Hz

        topic = self.get_parameter('cmd_vel_topic').value
        self.linear_speed = self.get_parameter('linear_speed').value
        self.angular_speed = self.get_parameter('angular_speed').value
        rate = self.get_parameter('publish_rate').value

        # Publisher and Timer
        self.publisher = self.create_publisher(Twist, topic, 10)
        self.timer = self.create_timer(1.0 / rate, self.timer_callback)

        # State variables
        self.current_linear = 0.0
        self.current_angular = 0.0

        self.print_usage()

    def print_usage(self):
        self.get_logger().info("=================================")
        self.get_logger().info("   ROS 2 Keyboard Teleop Node    ")
        self.get_logger().info("=================================")
        self.get_logger().info("  w/x : Increase/Decrease linear velocity")
        self.get_logger().info("  a/d : Increase/Decrease angular velocity")
        self.get_logger().info("  s   : Stop robot")
        self.get_logger().info("  q   : Quit")
        self.get_logger().info("=================================")

    def timer_callback(self):
        """Publishes the current velocity state at a fixed rate."""
        msg = Twist()
        msg.linear.x = self.current_linear
        msg.angular.z = self.current_angular
        self.publisher.publish(msg)

    def process_key(self, key):
        """Updates the velocity state based on the pressed key."""
        if key == 'w':
            self.current_linear = self.linear_speed
            self.current_angular = 0.0
        elif key == 'x':
            self.current_linear = -self.linear_speed
            self.current_angular = 0.0
        elif key == 'a':
            self.current_linear = 0.0
            self.current_angular = self.angular_speed
        elif key == 'd':
            self.current_linear = 0.0
            self.current_angular = -self.angular_speed
        elif key == 's':
            self.current_linear = 0.0
            self.current_angular = 0.0
        else:
            self.current_linear = 0.0
            self.current_angular = 0.0

    def stop_robot(self):
        """Sends a zero-velocity command to ensure the robot stops."""
        msg = Twist()
        msg.linear.x = 0.0
        msg.angular.z = 0.0
        self.publisher.publish(msg)
        self.get_logger().info("Robot stopped.")

def get_key(timeout=0.1):

    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        rlist, _, _ = select.select([sys.stdin], [], [], timeout)
        if rlist:
            return sys.stdin.read(1)
        return None
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

def main():
    rclpy.init()
    node = KeyboardTeleop()

    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)

    try:
        tty.setraw(fd)
        node.get_logger().info("Teleop started. Press 'q' to quit.")
        
        while rclpy.ok():
            key = get_key(timeout=0.1)
            
            if key is not None:
                node.process_key(key)
                if key == 'q':
                    break
                
            # Process ROS 2 callbacks (like the timer)
            rclpy.spin_once(node, timeout_sec=0)

    except KeyboardInterrupt:
        node.get_logger().info("KeyboardInterrupt received.")
    except Exception as e:
        node.get_logger().error(f"An error occurred: {e}")
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        
        node.stop_robot()
        
        node.get_logger().info("Shutting down Teleop node...")
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()