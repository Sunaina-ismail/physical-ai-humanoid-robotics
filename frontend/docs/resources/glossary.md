# Glossary

**Comprehensive terminology reference for Physical AI & Humanoid Robotics**

---

## A

**Action** - In robotics, an executable command or behavior that causes physical change in the robot or environment (e.g., moving motors, grasping objects, navigating to a location). In ROS 2, an action is a long-running request-response communication pattern with feedback.

**Actuator** - A mechanical device that converts electrical signals into physical motion. Common types include electric motors (servo, stepper, brushless DC), hydraulic cylinders, and pneumatic pistons.

**AMCL (Adaptive Monte Carlo Localization)** - A probabilistic localization algorithm that uses particle filters to estimate a robot's position within a known map by comparing sensor measurements (typically laser scans) against the map.

---

## B

**Behavior Tree** - A hierarchical control structure used in robotics for decision-making and task execution. Nodes represent actions, conditions, or control flow logic (sequence, fallback, parallel).

**BOM (Bill of Materials)** - A comprehensive list of all hardware components, quantities, specifications, and costs required to build a robot system.

---

## C

**Callback Function** - In ROS 2, a function that executes automatically when a specific event occurs (e.g., when a message arrives on a subscribed topic or when a timer triggers).

**Calibration** - The process of measuring and correcting sensor or actuator parameters to improve accuracy. Examples: camera intrinsic calibration, IMU bias calibration, robot kinematic calibration.

**Capstone Project** - A culminating project that integrates skills and knowledge from an entire course or curriculum, demonstrating comprehensive understanding and application ability.

**Closed-Loop Control** - A control system that uses sensor feedback to adjust commands and minimize error between desired and actual states. Contrast with open-loop control (no feedback).

**Configuration Space (C-space)** - The mathematical space representing all possible configurations of a robot, where each dimension corresponds to a degree of freedom (joint angle, position, orientation).

**Costmap** - A 2D or 3D grid representation of the environment where each cell has an associated cost value indicating traversability. Used by navigation algorithms to plan collision-free paths.

---

## D

**Dead Man Switch** - A safety mechanism that requires continuous operator presence/input to keep a system active. If the operator becomes incapacitated, the system automatically enters a safe state (e.g., motor cutoff with 100ms timeout).

**Degrees of Freedom (DOF)** - The number of independent parameters that define a robot's configuration. A humanoid arm typically has 7 DOF (shoulder: 3, elbow: 1, wrist: 3).

**Digital Twin** - A virtual replica of a physical robot or environment that accurately simulates dynamics, sensors, and behavior. Used for testing, validation, and training before deployment to hardware.

**DDS (Data Distribution Service)** - The middleware communication protocol used by ROS 2 for publish-subscribe messaging. Implementations include Fast DDS, CycloneDDS, and Connext DDS.

---

## E

**Embodied AI** - Artificial intelligence systems that physically interact with the real world through sensors and actuators, requiring real-time perception, decision-making, and action. See also: Physical AI.

**End-Effector** - The device at the end of a robotic arm that interacts with the environment (e.g., gripper, welding torch, camera, suction cup).

**EKF (Extended Kalman Filter)** - A nonlinear state estimation algorithm that extends the Kalman Filter for systems with nonlinear dynamics. Used in robot localization to fuse multiple sensor measurements (IMU, odometry, GPS).

---

## F

**Forward Kinematics** - Computing the position and orientation of a robot's end-effector given the joint angles. Contrast with inverse kinematics.

**Frontmatter** - Metadata at the beginning of a Markdown/MDX file, enclosed in `---` delimiters, containing structured information like title, prerequisites, learning outcomes, and tier support.

---

## G

**Gazebo** - An open-source 3D robotics simulator that provides physics simulation, sensor modeling, and visualization. Used for testing ROS 2 systems before hardware deployment.

**GPU (Graphics Processing Unit)** - A specialized processor optimized for parallel computation, essential for deep learning inference (computer vision, VLA models) on edge devices like Jetson Orin.

---

## H

**Humanoid Robot** - A robot with a human-like body structure, typically including a torso, two arms, two legs, and a head. Examples: Tesla Optimus, Boston Dynamics Atlas, Figure 02, Unitree H1.

---

## I

**IMU (Inertial Measurement Unit)** - A sensor that measures acceleration and angular velocity using accelerometers and gyroscopes. Often includes a magnetometer for orientation estimation.

**Inverse Kinematics (IK)** - Computing the joint angles required to place a robot's end-effector at a desired position and orientation. Often has multiple solutions or no solution (singularities).

**Isaac Sim** - NVIDIA's GPU-accelerated robotics simulator built on Omniverse, providing photorealistic rendering, physics simulation, and domain randomization for sim-to-real transfer.

---

## J

**Jetson Orin** - NVIDIA's edge AI computing platform for robotics, featuring GPU acceleration for deep learning inference, ROS 2 support, and low-power operation. Part of Tier B (Edge AI) in this textbook.

**Joint** - A mechanical connection between robot links that allows relative motion. Common types: revolute (rotational), prismatic (linear), spherical (ball-and-socket).

---

## K

**Kinematic Chain** - A sequence of rigid bodies (links) connected by joints, forming a robot's mechanical structure. Can be serial (open chain) or parallel (closed loops).

---

## L

**LiDAR (Light Detection and Ranging)** - A sensor that measures distances by emitting laser pulses and measuring time-of-flight. Used for 2D/3D mapping, obstacle detection, and localization.

**Localization** - Estimating a robot's position and orientation within a map or coordinate frame using sensor measurements (odometry, IMU, GPS, vision).

**Loose Coupling** - A software design principle where components interact through well-defined interfaces without direct dependencies. ROS 2's publish-subscribe pattern enables loose coupling.

---

## M

**Manipulation** - Robotic tasks involving grasping, moving, or otherwise physically interacting with objects in the environment.

**Message Type** - In ROS 2, the data structure definition for messages sent on topics (e.g., `std_msgs/Float32`, `sensor_msgs/Image`, `geometry_msgs/Twist`). Both publishers and subscribers must use matching message types.

**Motion Planning** - Computing a collision-free trajectory from a start configuration to a goal configuration, considering robot kinematics, dynamics, and environmental obstacles.

---

## N

**Nav2 (Navigation 2)** - The ROS 2 navigation framework providing costmap generation, path planning, path following, recovery behaviors, and localization for mobile robots.

**Node** - In ROS 2, an independent executable process that performs a specific task. Nodes communicate via topics, services, and actions.

---

## O

**Odometry** - Estimating a robot's position and velocity by integrating wheel encoder measurements or visual feature tracking over time. Accumulates drift error without correction.

**Open-Loop Control** - A control system that executes commands without using sensor feedback to verify results. Less accurate than closed-loop control but simpler and faster.

---

## P

**Physical AI** - AI systems embodied in physical robots that perceive and act in the real world, integrating perception (sensors), cognition (planning, learning), and action (actuators). See also: Embodied AI.

**Pose** - A robot's position and orientation in 3D space, typically represented as (x, y, z, roll, pitch, yaw) or as a transformation matrix.

**Publisher** - In ROS 2, a component that sends messages to a topic. Publishers operate independently of subscribers (loose coupling).

**Publish-Subscribe Pattern** - A communication pattern where publishers broadcast messages to topics without knowing who receives them, and subscribers listen to topics without knowing who sends messages.

---

## Q

**QoS (Quality of Service)** - Configurable communication policies in ROS 2 that control reliability, durability, history depth, and latency. Examples: RELIABLE vs. BEST_EFFORT reliability.

**Quaternion** - A mathematical representation of 3D rotation using four values (w, x, y, z), avoiding gimbal lock problems of Euler angles. Used extensively in robotics for orientation.

---

## R

**rclpy** - The ROS 2 Python client library, providing APIs for creating nodes, publishers, subscribers, services, actions, and timers.

**RGB-D Camera** - A camera that captures both color (RGB) and depth (D) information for each pixel. Used for 3D perception, object detection, and mapping.

**Robot Operating System 2 (ROS 2)** - An open-source middleware framework for building modular, distributed robotics systems. Provides communication (topics, services, actions), tools, and libraries.

---

## S

**Sensor-Action Loop** - The fundamental cycle of robotics: sense the environment → perceive state → plan action → execute action → sense again. Also called sense-plan-act loop.

**Service** - In ROS 2, a request-response communication pattern for synchronous interactions (e.g., "is the door open?" → yes/no). Contrast with topics (asynchronous streaming).

**Sim-to-Real** - The workflow of developing robot systems in simulation (Gazebo, Isaac Sim) and transferring them to physical hardware, accounting for simulation-reality gaps.

**SLAM (Simultaneous Localization and Mapping)** - Building a map of an unknown environment while simultaneously tracking the robot's location within that map. Foundation of autonomous navigation.

**Subscriber** - In ROS 2, a component that receives messages from a topic by registering a callback function. Multiple subscribers can listen to the same topic.

---

## T

**Three-Tier System** - The pedagogical structure of this textbook:
- **Tier A (Simulation)**: CPU-only, accessible to all learners, using Gazebo/Isaac Sim
- **Tier B (Edge AI)**: Jetson Orin deployment for GPU-accelerated perception
- **Tier C (Physical Robot)**: Real hardware deployment on Unitree humanoid robots

**Topic** - In ROS 2, a named communication channel for asynchronous message passing. Topics have a name (e.g., `/camera/image_raw`) and a message type (e.g., `sensor_msgs/Image`).

**Transform (TF)** - In ROS 2, the relationship between coordinate frames (position + orientation). The TF system tracks transforms between all frames in a robot (sensors, joints, end-effector, world).

**Twist** - A message type (`geometry_msgs/Twist`) representing linear and angular velocity in 3D space. Commonly used for robot velocity commands.

---

## U

**URDF (Unified Robot Description Format)** - An XML-based format for describing robot kinematics, dynamics, sensors, and visual/collision geometry. Used by ROS 2, Gazebo, and motion planning libraries.

**Unitree H1** - A commercial humanoid robot platform with 19 degrees of freedom, used in this textbook's Tier C (Physical Robot) pathway for real-world deployment.

---

## V

**Vision-Language-Action (VLA)** - A class of multimodal AI models that process visual and language inputs to predict robotic actions. Examples: RT-2, PaLM-E, OpenVLA.

**VSLAM (Visual SLAM)** - SLAM using cameras as the primary sensor, extracting visual features and tracking their 3D positions over time. Examples: ORB-SLAM3, RTAB-Map.

---

## W

**Workspace** - The set of all positions and orientations that a robot's end-effector can reach. Determined by link lengths, joint limits, and kinematic structure.

---

## Further Resources

### Official Documentation
- [ROS 2 Concepts](https://docs.ros.org/en/humble/Concepts.html) - Core ROS 2 terminology
- [Nav2 Glossary](https://navigation.ros.org/glossary.html) - Navigation-specific terms
- [Gazebo Documentation](https://gazebosim.org/docs) - Simulation terminology

### Robotics References
- [Robotics Glossary (Springer)](https://link.springer.com/referenceworkentry/10.1007/978-3-319-32552-1) - Academic terminology
- [Modern Robotics Textbook](http://hades.mech.northwestern.edu/index.php/Modern_Robotics) - Mathematical foundations

---

**Last Updated**: 2025-12-05
**License**: CC BY-SA 4.0
