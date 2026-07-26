# 🤖 Autonomous Ball Rover

An adapted and extended ROS 2 mobile robot simulation that combines autonomous navigation, SLAM, LiDAR perception, and computer vision-based yellow ball tracking.

The robot autonomously patrols predefined waypoints using Nav2. When it detects a yellow ball, it interrupts its patrol, follows the ball, and automatically resumes patrolling when the ball is lost.

---

## 📸 Project Overview

<!-- Add a main Gazebo screenshot here -->
<!-- Recommended filename: media/hero.png -->

![Autonomous Ball Rover](media/hero.png)

---

## 🎥 Demo

<!-- Add a GIF or short video showing the complete behavior -->
<!-- Recommended filename: media/demo.gif -->

![Autonomous Ball Rover Demo](media/demo.gif)

### Autonomous Behavior

```text
┌──────────────────────┐
│      PATROLLING      │
│   Nav2 + Waypoints   │
└──────────┬───────────┘
           │
           │ Yellow Ball Detected
           ▼
┌──────────────────────┐
│    FOLLOWING BALL    │
│    OpenCV Tracking   │
└──────────┬───────────┘
           │
           │ Ball Lost
           ▼
┌──────────────────────┐
│      PATROLLING      │
└──────────────────────┘
````

---

## ✨ Features

* 🤖 Autonomous mobile robot simulation
* 🗺️ SLAM-based mapping
* 🧭 LiDAR-based environment perception
* 📍 Autonomous navigation using Nav2
* 🟡 Yellow ball detection using computer vision
* 🎯 Autonomous ball-following behavior
* 🔄 Automatic switching between navigation and ball tracking
* 🧠 State Machine-based behavior control
* 🚗 Modified custom robot design
* 🌍 Gazebo simulation environment
* 👁️ Camera-based object detection
* 🚀 Unified system startup through a main launch file
* ⚙️ ROS 2 Humble compatible

---

## 🧠 How It Works

The robot operates using an autonomous behavior system that combines Nav2 navigation with computer vision-based ball tracking.

### 1. Autonomous Patrolling

The robot starts by navigating between predefined waypoints using **Nav2**.

While patrolling, the camera continuously searches for a yellow ball.

```text
Start
  │
  ▼
Patrolling
  │
  ├── Yellow Ball Not Detected
  │        │
  │        ▼
  │   Continue Patrolling
  │
  └── Yellow Ball Detected
           │
           ▼
      Follow the Ball
```

<!-- Add a screenshot showing the robot patrolling in Gazebo -->

<!-- Recommended filename: media/patrolling.png -->

![Autonomous Patrolling](media/patrolling.png)

---

### 2. Yellow Ball Detection

The robot uses camera data and computer vision to detect a yellow ball.

The image processing pipeline identifies the yellow region and determines the position of the ball in the camera frame.

```text
Camera Image
      │
      ▼
Image Processing
      │
      ▼
Yellow Color Filtering
      │
      ▼
Ball Detection
      │
      ▼
Ball Position
```

<!-- Add a screenshot showing the yellow ball detection -->

<!-- Recommended filename: media/ball-detection.png -->

![Yellow Ball Detection](media/ball-detection.png)

---

### 3. Ball Following

When a yellow ball is detected, the robot switches from autonomous navigation to ball-following mode.

The robot adjusts its movement according to the ball's position in the camera image.

```text
Ball Position        Robot Behavior
────────────────────────────────────
Left                 Turn Left
Center               Move Forward
Right                Turn Right
Not Detected         Resume Patrol
```

<!-- Add a screenshot showing the robot following the yellow ball -->

<!-- Recommended filename: media/ball-following.png -->

![Ball Following](media/ball-following.png)

---

### 4. Returning to Patrol

When the ball is no longer visible, the robot automatically exits the ball-following state and returns to autonomous patrolling.

This allows the robot to continuously explore the environment and search for the ball.

---

## 🧠 State Machine

The robot's behavior is controlled using a state-based architecture.

```text
┌───────────────┐
│   PATROLLING  │
└───────┬───────┘
        │
        │ Yellow Ball Detected
        ▼
┌───────────────┐
│ FOLLOWING BALL│
└───────┬───────┘
        │
        │ Ball Lost
        ▼
┌───────────────┐
│   PATROLLING  │
└───────────────┘
```

The state machine allows the robot to dynamically change its behavior according to the environment.

---

## 🏗️ System Architecture

```text
                    ┌──────────────┐
                    │    Camera    │
                    └──────┬───────┘
                           │
                           ▼
                    ┌──────────────┐
                    │ Ball Tracker │
                    │    OpenCV    │
                    └──────┬───────┘
                           │
                           ▼
                    ┌──────────────┐
                    │ State Machine│
                    └──────┬───────┘
                           │
             ┌─────────────┴─────────────┐
             │                           │
             ▼                           ▼
      ┌──────────────┐           ┌──────────────┐
      │     Nav2     │           │ Ball Follow  │
      │  Navigation  │           │   Control    │
      └──────┬───────┘           └──────┬───────┘
             │                           │
             └─────────────┬─────────────┘
                           ▼
                    ┌──────────────┐
                    │ Mobile Robot │
                    └──────────────┘
```

---

## 🗺️ SLAM and Navigation

The robot uses a LiDAR sensor to perceive the simulated environment.

**SLAM** is used to create a map of the environment, while **Nav2** is used for autonomous navigation and waypoint-based patrolling.

The navigation system allows the robot to move autonomously without direct manual control.

<!-- Add an RViz screenshot showing the map, LiDAR scan, and robot -->

<!-- Recommended filename: media/slam-navigation.png -->

![SLAM and Navigation](media/slam-navigation.png)

---

## 🧰 Technologies

| Technology   | Purpose                             |
| ------------ | ----------------------------------- |
| ROS 2 Humble | Robot middleware and communication  |
| Gazebo       | Robot simulation                    |
| Nav2         | Autonomous navigation               |
| SLAM Toolbox | Mapping and localization            |
| LiDAR        | Environment perception              |
| OpenCV       | Image processing and ball detection |
| Python       | ROS 2 nodes and control logic       |
| RViz2        | Visualization and debugging         |

---

## 📁 Project Structure

```text
autonomous-ball-rover/
│
├── ball_rover/
│   ├── config/
│   ├── description/
│   ├── launch/
│   │   └── bringup.launch.py
│   ├── maps/
│   ├── rviz/
│   ├── scripts/
│   ├── worlds/
│   └── ...
│
├── ball_tracker/
│   ├── detect_ball.py
│   ├── follow_ball.py
│   ├── process_image.py
│   ├── state_machine.py
│   └── ...
│
├── media/
│   ├── hero.png
│   ├── demo.gif
│   ├── patrolling.png
│   ├── ball-detection.png
│   ├── ball-following.png
│   └── slam-navigation.png
│
└── README.md
```

---

## ⚙️ Requirements

* Ubuntu 22.04
* ROS 2 Humble
* Gazebo
* RViz2
* Nav2
* SLAM Toolbox
* OpenCV
* Python 3

---

## 🚀 Installation

Create a ROS 2 workspace:

```bash
mkdir -p ~/autonomous_ball_rover_ws/src
cd ~/autonomous_ball_rover_ws/src
```

Clone the repository:

```bash
git clone https://github.com/moamir369/ros2-autonomous-ball-rover.git
```

Navigate to the workspace:

```bash
cd ~/autonomous_ball_rover_ws
```

Build the project:

```bash
colcon build
```

Source the workspace:

```bash
source install/setup.bash
```

---

## ▶️ Running the Project

The complete system can be launched using the main launch file:

```bash
ros2 launch ball_rover bringup.launch.py
```

The `bringup.launch.py` file serves as the main entry point for launching the required components of the robot system.

---

## 🔄 Autonomous Workflow

```text
┌─────────────────────┐
│       START         │
└──────────┬──────────┘
           ▼
┌─────────────────────┐
│   Start Simulation   │
└──────────┬──────────┘
           ▼
┌─────────────────────┐
│      PATROLLING     │
│    Nav2 Waypoints   │
└──────────┬──────────┘
           │
           ▼
     ┌───────────┐
     │ Ball      │
     │ Detected? │
     └─────┬─────┘
           │
     ┌─────┴─────┐
     │           │
    No          Yes
     │           │
     ▼           ▼
Continue    Stop Patrol
Patrolling      │
                ▼
        ┌───────────────┐
        │  Follow Ball  │
        └───────┬───────┘
                │
                ▼
          Ball Lost?
                │
                ▼
        Resume Patrolling
```

---

## 🔧 Adaptations and Extensions

This project is based on an existing mobile robot project and was adapted and extended to support ROS 2 Humble and additional autonomous behaviors.

### Main Modifications

* Adapted the project to work with **ROS 2 Humble**.
* Modified the robot's visual design.
* Integrated **Nav2** with the ball-tracking system.
* Added autonomous patrolling between predefined waypoints.
* Added yellow ball detection using computer vision.
* Added autonomous ball-following behavior.
* Implemented a State Machine for behavior management.
* Added automatic switching from patrolling to ball following when a yellow ball is detected.
* Added automatic return to patrolling when the ball is lost.
* Integrated the complete system through the main `bringup.launch.py` launch file.

---

## 🎯 Project Goals

The main goal of this project is to combine autonomous navigation and computer vision into a single robotic behavior system.

The project demonstrates how a mobile robot can:

* Navigate autonomously through a simulated environment.
* Build and use maps using SLAM.
* Use LiDAR for environment perception.
* Detect a specific object using computer vision.
* Change its behavior based on visual input.
* Combine Nav2 navigation with object-following behavior.

---

## 📚 Acknowledgments

This project is based on and adapted from the
[Mobile Robot Project by Articulated Robotics](https://articulatedrobotics.xyz/tutorials/mobile-robot/project-overview).

The original project was used as the foundation for the ROS 2 mobile robot simulation.

This version was adapted for **ROS 2 Humble** and extended with additional functionality, including autonomous patrolling, yellow ball detection, ball-following behavior, and state-based behavior switching.

The original project structure and core concepts are credited to **Articulated Robotics**.

---

## 👨‍💻 Author

**Muhammet Emir Hallek**

Computer Engineering Student

Interested in:

* ROS 2
* Robotics
* Autonomous Systems
* Computer Vision
* Embedded Systems
* Artificial Intelligence

---

## 📄 License

This project is intended for educational and research purposes.

The original project and concepts are credited to Articulated Robotics.

Please refer to the original project's licensing terms where applicable.

````
