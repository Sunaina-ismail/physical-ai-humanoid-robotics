---
id: module-3
title: "Module 3: Navigation & Embodied AI"
description: "Weeks 8-10 Content | Tier Support: 🟢 A • 🔵 B • 🟣 C"
---

# Module 3: Navigation & Embodied AI

**Duration**: Weeks 8-10 | **Tier Support**: 🟢 A • 🔵 B • 🟣 C

## Learning Outcome

By the end of Module 3, you will **deploy voice-to-navigation pipelines using Nav2 and VSLAM**, enabling robots to autonomously map environments, localize themselves, plan collision-free paths, and respond to natural language commands like "Go to the kitchen."

---

## Overview

Module 3 bridges **perception** and **action** by teaching you how robots navigate autonomously in unknown environments. You'll master:

- **SLAM (Simultaneous Localization and Mapping)**: Building maps while tracking robot position
- **Nav2 Stack**: ROS 2's production-grade navigation framework used in warehouses, hospitals, and homes
- **Sensor Fusion**: Combining LiDAR, cameras, IMU, and wheel odometry for robust localization
- **VSLAM (Visual SLAM)**: Camera-only navigation for GPS-denied environments
- **Voice-Controlled Navigation**: Integrating speech recognition with Nav2 waypoint following

This is where your ROS 2 knowledge (Module 1) and simulation skills (Module 2) converge into **real autonomous systems**.

---

## Why This Module Matters

**Autonomous navigation is the foundation of mobile robotics**:
- **Warehouse robots** (Amazon, Fetch Robotics) use Nav2 for goods delivery
- **Household robots** (iRobot, Boston Dynamics Spot) map homes and navigate to rooms
- **Humanoid robots** (Tesla Optimus, Unitree G1) require VSLAM for dynamic environments
- **Self-driving cars** use HD maps + localization (similar to SLAM)

By the end of this module, you'll deploy systems that:
- Map a simulated office building (Tier A)
- Navigate a real room using Jetson + LiDAR (Tier B)
- Command a Unitree robot with voice: "Go to the charging station" (Tier C)

---

## Week-by-Week Breakdown

### Week 8: Nav2 Architecture & Isaac Sim Navigation
**Chapters**:
- [Chapter 16: Navigation Concepts](./week-8/ch16-navigation-concepts.mdx)
- [Chapter 17: Nav2 Stack Overview](./week-8/ch17-nav2-stack-overview.mdx) (Costmaps, Planners, Controllers)

**Key Concepts**:
- Nav2 behavior trees (navigate to pose, follow waypoints)
- Global planner (A*, Theta*, Smac Hybrid) vs. local planner (DWB, TEB, MPPI)
- Costmaps (static map, inflation layer, obstacle layer)
- Recovery behaviors (spinning, backing up) when stuck
- Isaac Sim integration with Nav2 for testing

**Tier A**: Deploy Nav2 in Gazebo with 2D LiDAR and a static map
**Tier B**: Run Nav2 on Jetson with real RPLidar in an office
**Tier C**: Integrate Nav2 with Unitree locomotion controller

**Milestone**: Robot autonomously navigates from Point A to Point B, avoiding obstacles and re-planning when blocked

---

### Week 9: SLAM Algorithms & Map Building
**Chapters**:
- [Chapter 18: SLAM Fundamentals](./week-9/ch18-slam-fundamentals.mdx) (EKF-SLAM, Graph-SLAM)
- [Chapter 19: GMapping and Cartographer](./week-9/ch19-gmapping-cartographer.mdx) (Practical SLAM with GMapping and Cartographer)
- [Chapter 20: RTAB-Map for RGB-D SLAM](./week-9/ch20-rtab-map.mdx) (RGB-D SLAM using depth cameras)

**Key Concepts**:
- **GMapping**: 2D laser-based SLAM (lightweight, good for structured environments)
- **Cartographer**: 2D/3D SLAM with loop closure (Google's algorithm)
- **RTAB-Map**: RGB-D SLAM using depth cameras (Intel RealSense)
- Map saving/loading (`map_server`)
- Localization with AMCL (Adaptive Monte Carlo Localization)

**Tier A**: Build a map of a Gazebo world with GMapping, save it, then localize with AMCL
**Tier B**: Create a real office map using Jetson + RPLidar, then autonomously navigate it
**Tier C**: Use RTAB-Map on Unitree's built-in cameras for visual SLAM

**Milestone**: Complete a mapping session → save map → re-localize in saved map → navigate autonomously

---

### Week 10: Visual SLAM & Voice-Controlled Navigation
**Chapters**:
- [Chapter 21: VSLAM with ORB-SLAM3 and OpenVSLAM](./week-10/ch21-vslam-orb-slam.mdx)
- [Chapter 22: Sensor Fusion (IMU + Visual Odometry)](./week-10/ch22-sensor-fusion-vio.mdx)
- [Chapter 23: Voice-to-Navigation Pipeline](./week-10/ch23-voice-to-navigation.mdx)

**Key Concepts**:
- **VSLAM**: Camera-only SLAM (no LiDAR required)
- **ORB-SLAM3**: State-of-the-art monocular/stereo/RGB-D SLAM
- **VIO (Visual-Inertial Odometry)**: Fusing camera + IMU for drift reduction
- Speech recognition (Whisper, Vosk) → natural language processing → Nav2 waypoints
- Dynamic obstacle avoidance with real-time costmap updates

**Tier A**: Run ORB-SLAM3 with Gazebo camera, send navigation goals via Python script
**Tier B**: Deploy VSLAM on Jetson with Intel RealSense, control with voice commands
**Tier C**: Full pipeline on Unitree: "Go to the kitchen" → VSLAM → Nav2 → locomotion

**Milestone**: Command robot via voice ("Navigate to the meeting room") and watch it autonomously execute

---

## Three-Tier Learning Path

### 🟢 Tier A: Simulation-Based Navigation (Required)
**Hardware**: Laptop with Ubuntu 22.04 (or Docker)
**Software**: ROS 2 Humble, Nav2, Gazebo, GMapping or Cartographer

Tier A provides complete navigation training:
- **2D SLAM**: GMapping or slam_toolbox for laser-based mapping
- **Nav2**: Full behavior tree navigation with recovery behaviors
- **Simulated sensors**: 2D LiDAR, RGB cameras, wheel odometry
- **Scenario testing**: Test in office, warehouse, and outdoor Gazebo worlds

**Key advantage**: Test 100 scenarios (narrow hallways, dynamic obstacles, sensor failures) risk-free

---

### 🔵 Tier B: Real Sensors + Jetson Deployment (Optional Extension)
**Hardware**: Jetson Orin + RPLidar A1/A3 or Intel RealSense D435i
**Software**: Nav2 on Jetson, RTAB-Map or ORB-SLAM3, TensorRT for acceleration

Tier B adds:
- **Real sensor noise**: Handle LiDAR dropouts, camera motion blur, IMU drift
- **Dynamic obstacles**: People walking, doors opening/closing
- **Hardware constraints**: Battery life, thermal throttling, real-time deadlines
- **Integration**: ROS 2 bridge to motor controllers (e.g., Clearpath Husky, TurtleBot 4)

**Use case**: Build a home delivery robot that maps your apartment and delivers items on command

---

### 🟣 Tier C: Unitree Humanoid Navigation (Optional Extension)
**Hardware**: Unitree Go2 or G1 + Isaac Sim for validation
**Software**: Unitree SDK, Nav2 integration, VSLAM stack

Tier C adds:
- **Humanoid locomotion**: Nav2 velocity commands → bipedal walking gaits
- **Visual SLAM**: Camera-only navigation (Unitree robots have built-in stereo cameras)
- **Safety interlocks**: Stop navigation if robot loses balance
- **Voice control**: Integrate speech recognition with Nav2 action servers

**Use case**: Deploy a G1 humanoid that navigates an office, avoiding obstacles and responding to voice commands

**⚠️ Safety**: Test all navigation policies in Isaac Sim digital twin before physical deployment. Always have emergency stop ready.

---

## Prerequisites

Before starting Module 3, you should have completed:

- **Module 1**: ROS 2 fundamentals, tf2 transforms, action servers
- **Module 2**: Gazebo simulation, sensor visualization in RViz
- **Comfort with coordinate frames**: Understanding `map`, `odom`, `base_link`

**Checkpoint**: Can you spawn a robot in Gazebo with a LiDAR sensor and visualize scan data in RViz? If yes, you're ready.

---

## Learning Resources

### Official Documentation
- [Nav2 Documentation](https://navigation.ros.org/)
- [slam_toolbox](https://github.com/SteveMacenski/slam_toolbox) (recommended for ROS 2)
- [Cartographer ROS](https://google-cartographer-ros.readthedocs.io/)
- [ORB-SLAM3](https://github.com/UZ-SLAMLab/ORB_SLAM3)
- [RTAB-Map](http://introlab.github.io/rtabmap/)

### Key Concepts
- **SLAM**: Simultaneous Localization and Mapping (building a map while tracking position)
- **AMCL**: Adaptive Monte Carlo Localization (particle filter for robot localization)
- **Costmap**: 2D grid representing obstacle occupancy (static map + dynamic obstacles + inflation)
- **Behavior Tree**: Hierarchical state machine for navigation decision-making (Nav2 uses this)
- **VSLAM**: Visual SLAM (camera-only, no LiDAR)

### Community Resources
- [Nav2 Slack](https://navigation2.slack.com/) (official support channel)
- [ROS Discourse - Navigation](https://discourse.ros.org/c/navigation/44)
- [Cyrill Stachniss YouTube](https://www.youtube.com/c/CyrillStachniss) (SLAM theory lectures)

---

## Assessment & Progression

### Knowledge Checks
- **Quizzes**: 70% passing threshold for each chapter
- **Hands-On Exercises**:
  - Week 8: Configure Nav2 parameters for narrow hallways vs. open spaces
  - Week 9: Build and save a map, then localize with AMCL
  - Week 10: Integrate speech recognition with Nav2 waypoint following
- **Capstone Preview**: Create a multi-room navigation system with voice control

### How to Know You're Ready for Module 4
You should be able to:
1. ✅ Explain the difference between global planners (A*) and local planners (DWB)
2. ✅ Build a map using SLAM, save it, and re-localize in it
3. ✅ Configure Nav2 costmaps (inflation radius, obstacle layers)
4. ✅ Integrate sensor data (LiDAR or camera) with Nav2
5. ✅ Debug navigation failures using RViz visualizations

If you can deploy a voice-controlled navigation system (even in simulation), you're ready for **Module 4: Vision-Language-Action Systems**.

---

## What's Next?

After completing Module 3:
- **Module 4** integrates **Vision-Language-Action (VLA) models** like OpenVLA and RT-2
- You'll replace manual waypoint commands with natural language: "Bring me a coffee from the kitchen"
- VLA models will plan navigation paths, manipulate objects, and chain multi-step tasks

**Why navigation matters for VLA**: Models like RT-2 require robust navigation stacks to execute physical tasks. Module 3 provides that foundation.

**Start Learning**: Proceed to [Chapter 16: Isaac Sim Navigation Concepts](./week-8/ch16-isaac-sim-concepts.mdx)

---

## Chapter List

### Week 8: Nav2 & Isaac Sim
- [Chapter 16: Navigation Concepts](./week-8/ch16-navigation-concepts.mdx)
- [Chapter 17: Nav2 Stack Overview](./week-8/ch17-nav2-stack-overview.mdx)

### Week 9: SLAM & Mapping
- [Chapter 18: SLAM Fundamentals](./week-9/ch18-slam-fundamentals.mdx)
- [Chapter 19: GMapping and Cartographer](./week-9/ch19-gmapping-cartographer.mdx)
- [Chapter 20: RTAB-Map for RGB-D SLAM](./week-9/ch20-rtab-map.mdx)

### Week 10: VSLAM & Voice Control
- [Chapter 21: VSLAM with ORB-SLAM3 and OpenVSLAM](./week-10/ch21-vslam-orb-slam.mdx)
- [Chapter 22: Sensor Fusion (IMU + Visual Odometry)](./week-10/ch22-sensor-fusion-vio.mdx)
- [Chapter 23: Voice-to-Navigation Pipeline](./week-10/ch23-voice-to-navigation.mdx)

---

**Ready to build autonomous navigation systems?** Start with [Chapter 16: Navigation Concepts](./week-8/ch16-navigation-concepts.mdx) →
