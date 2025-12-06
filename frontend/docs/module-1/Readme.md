---
id: module-1
title: "Module 1: Foundations of Physical AI"
description: "Weeks 1-5 Content | Tier Support: 🟢 A • 🔵 B • 🟣 C"
---

# Module 1: Foundations of Physical AI

**Duration**: Weeks 1-5 | **Tier Support**: 🟢 A • 🔵 B • 🟣 C

## Learning Outcome

By the end of Module 1, you will **build and test your first ROS 2 robot in simulation**, understanding the foundational architecture, communication patterns, and computational principles that power modern robotics systems.

---

## Overview

Module 1 establishes the **conceptual and technical foundations** for Physical AI—the paradigm where embodied robots use AI to perceive, reason, and act in the physical world. You'll learn:

- **ROS 2 Architecture**: Nodes, topics, services, actions, and the distributed publish-subscribe model
- **Python for Robotics**: Object-oriented patterns, asynchronous programming, and NumPy for sensor data processing
- **Digital Signal Processing (DSP)**: Filtering, Fourier transforms, and real-time sensor interpretation
- **Robot Modeling**: URDF files, coordinate transforms (tf2), and kinematic chains
- **Testing & CI/CD**: pytest, launch testing, and continuous integration for robotics code

This module is designed for **absolute beginners** in robotics—no prior ROS or robotics experience required. If you're comfortable with Python basics and command-line tools, you're ready to start.

---

## Why This Module Matters

Modern robotics systems like **Tesla Optimus**, **Unitree G1**, and **Boston Dynamics Atlas** all rely on the same foundational concepts you'll learn here:

- **Distributed computation** (ROS 2 nodes) enables modular, fault-tolerant systems
- **Coordinate transforms** (tf2) solve the "where is the object relative to the robot?" problem
- **DSP** turns noisy sensor streams into actionable data
- **Simulation-first development** (Tier A) allows rapid iteration before deploying to expensive hardware

By mastering these foundations in **simulation** (Tier A), you build the mental models needed to deploy on **edge devices** (Tier B) or **physical robots** (Tier C) in later modules.

---

## Week-by-Week Breakdown

### Week 1: Physical AI Paradigm & ROS 2 Basics
**Chapters**:
- [Chapter 1: Introduction to Physical AI](./week-1/ch01-physical-ai-intro.mdx)
- [Chapter 2: ROS 2 Nodes and Topics](./week-1/ch02-ros2-nodes-topics.mdx)

**Key Concepts**:
- What is Physical AI? (vs. traditional robotics and cloud AI)
- ROS 2 graph architecture and the publish-subscribe pattern
- Creating your first publisher and subscriber nodes

**Tier A**: Run ROS 2 Humble in Docker or native Ubuntu with CPU-only examples
**Tier B**: Install ROS 2 on Jetson Orin with hardware-accelerated libraries
**Tier C**: Connect to Unitree Go2/G1 SDK and explore pre-existing ROS 2 topics

**Milestone**: Run a "Hello, ROS 2!" publisher-subscriber pair and visualize the graph with `rqt_graph`

---

### Week 2: Python for Robotics & DSP Fundamentals
**Chapters**:
- Chapter 3: Python Patterns for Robotics
- Chapter 4: Digital Signal Processing Basics

**Key Concepts**:
- Object-oriented design for ROS 2 nodes (classes, inheritance)
- NumPy arrays for sensor data (IMU, LiDAR, camera buffers)
- Low-pass filters, moving averages, and noise reduction
- Fourier transforms for frequency analysis

**Tier A**: Process simulated IMU data with NumPy
**Tier B**: Stream real IMU data from Jetson sensors and apply filters
**Tier C**: Analyze motor encoder signals from Unitree robots

**Milestone**: Build an IMU data processor that filters accelerometer noise and detects motion patterns

---

### Week 3: ROS 2 Services, Actions & Lifecycle
**Chapters**:
- Chapter 5: ROS 2 Services and Actions
- Chapter 6: Lifecycle Nodes and Managed Systems

**Key Concepts**:
- Services vs. topics (request-response vs. continuous streams)
- Actions for long-running tasks (with feedback and cancellation)
- Lifecycle nodes (unconfigured → inactive → active states)
- Error handling and graceful degradation

**Tier A**: Create a "move robot" action server in simulation
**Tier B**: Implement emergency stop service on Jetson
**Tier C**: Use Unitree SDK actions for locomotion control

**Milestone**: Deploy a managed navigation system that transitions through lifecycle states and handles cancellation requests

---

### Week 4: Transforms (tf2) & Robot Models (URDF)
**Chapters**:
- Chapter 7: Coordinate Transforms with tf2
- Chapter 8: URDF Robot Descriptions

**Key Concepts**:
- Why coordinate frames matter (base_link, odom, map, camera_frame)
- tf2 transform trees and parent-child relationships
- URDF syntax (links, joints, visual/collision geometry)
- Using `robot_state_publisher` to broadcast transforms

**Tier A**: Create a URDF model of a simple 2-wheeled robot in Gazebo
**Tier B**: Import Jetson camera extrinsics into tf2 tree
**Tier C**: Load Unitree URDF models and verify joint transforms

**Milestone**: Build a complete robot URDF with sensors and visualize in RViz with live tf2 updates

---

### Week 5: Testing, Debugging & CI/CD
**Chapters**:
- Chapter 9: Unit Testing with pytest
- Chapter 10: Launch Testing and Integration Tests

**Key Concepts**:
- pytest fixtures for ROS 2 nodes
- Launch testing (spinning up nodes and validating outputs)
- GitHub Actions for continuous integration
- Debugging with `ros2 topic echo`, `ros2 node info`, and `rqt`

**Tier A**: Write unit tests for publisher/subscriber nodes
**Tier B**: Add hardware-in-the-loop tests for Jetson sensors
**Tier C**: Create safety validation tests for Unitree motor commands

**Milestone**: Set up CI/CD pipeline that runs automated tests on every commit

---

## Three-Tier Learning Path

### 🟢 Tier A: Simulation (Required)
**Hardware**: Laptop with Ubuntu 22.04 (native or WSL2) or Docker
**Software**: ROS 2 Humble, Python 3.10+, Gazebo Classic or Gazebo Sim

All Week 1-5 content is fully accessible in Tier A. You'll:
- Run ROS 2 nodes in simulated time
- Process synthetic sensor data (IMU, LiDAR, cameras)
- Use Gazebo's physics engine for robot testing
- Complete all exercises and quizzes without hardware

**Recommended**: Use Docker for reproducible environments (see [ROS 2 Setup Guide](../resources/ros2-setup.md))

---

### 🔵 Tier B: Edge AI (Optional Extension)
**Hardware**: NVIDIA Jetson Orin Nano (8GB) or Orin NX (16GB)
**Software**: JetPack 5.1+, ROS 2 Humble, real sensors (Intel RealSense D435i, RPLidar A1)

Tier B extensions add:
- Real sensor integration (camera drivers, LiDAR nodes)
- TensorRT-accelerated inference (preview for Module 4)
- Power and thermal management for edge deployment
- Hardware-in-the-loop testing

**When to upgrade**: After completing Tier A content for Weeks 1-3 and feeling confident with ROS 2 basics

---

### 🟣 Tier C: Physical Robot (Optional Extension)
**Hardware**: Unitree Go2 or Unitree G1 humanoid robot
**Software**: Unitree SDK, ROS 2 bridge, safety monitoring stack

Tier C extensions add:
- Direct motor control with safety interlocks (Dead Man Switch)
- Real-world coordinate transform validation
- Sensor calibration for physical hardware
- Emergency stop protocols and fault tolerance

**When to upgrade**: After completing Module 2 (Simulation) to understand digital twin validation before physical deployment

**⚠️ Safety Warning**: Tier C requires controlled environments, emergency stop buttons, and adherence to safety protocols. Never run untested code on physical robots.

---

## Prerequisites

Before starting Module 1, you should be familiar with:

- **Python Basics**: Variables, functions, classes, lists, dictionaries
- **Command Line**: Navigating directories, running scripts, environment variables
- **Git**: Cloning repositories, committing changes (basic workflow)
- **Linear Algebra** (helpful): Vectors, matrices, dot products

**Not Required**:
- Prior ROS or robotics experience
- Mechanical or electrical engineering background
- Advanced mathematics (calculus, differential equations)

**Need Review?** See the [Prerequisites Guide](../resources/prerequisites.md) for recommended tutorials.

---

## Learning Resources

### Official Documentation
- [ROS 2 Humble Docs](https://docs.ros.org/en/humble/)
- [rclpy API Reference](https://docs.ros2.org/latest/api/rclpy/)
- [Gazebo Tutorials](https://gazebosim.org/docs)

### Recommended Reading
- "Programming Robots with ROS" by Morgan Quigley (foundational concepts)
- "Probabilistic Robotics" by Thrun, Burgard, Fox (advanced, for Week 9+)

### Community Support
- [ROS Discourse](https://discourse.ros.org/) - Official forum
- [Robotics Stack Exchange](https://robotics.stackexchange.com/) - Q&A site
- [r/ROS](https://reddit.com/r/ROS) - Community discussions

---

## Assessment & Progression

### Knowledge Checks
- **Quizzes**: Each chapter includes a quiz with a **70% passing threshold**
- **Exercises**: Hands-on coding challenges with acceptance criteria (self-graded)
- **Capstone Preview**: Week 5 ends with a mini-project integrating all concepts

### How to Know You're Ready for Module 2
You should be able to:
1. ✅ Create custom ROS 2 nodes with publishers, subscribers, services, and actions
2. ✅ Explain the difference between topics (streaming data) and services (request-response)
3. ✅ Build a URDF model and visualize it with correct transforms in RViz
4. ✅ Write unit tests for ROS 2 nodes using pytest
5. ✅ Debug issues using `ros2 topic list`, `ros2 node info`, and `rqt_graph`

If you can confidently do all of the above, you're ready to dive into **Module 2: Simulation & Digital Twins**.

---

## What's Next?

After completing Module 1:
- **Module 2** teaches you to build high-fidelity simulations (Gazebo, Isaac Sim) for rapid iteration
- **Module 3** applies your ROS 2 skills to SLAM, navigation, and sensor fusion
- **Module 4** integrates Vision-Language-Action models for natural language control

**Start Learning**: Proceed to [Chapter 1: Introduction to Physical AI](./week-1/ch01-physical-ai-intro.mdx)

---

## Chapter List

### Week 1: Physical AI & ROS 2 Basics
- [Chapter 1: Introduction to Physical AI](./week-1/ch01-physical-ai-intro.mdx)
- [Chapter 2: ROS 2 Nodes and Topics](./week-1/ch02-ros2-nodes-topics.mdx)

### Week 2: Python & DSP
- Chapter 3: Python Patterns for Robotics *(Coming Soon)*
- Chapter 4: Digital Signal Processing Basics *(Coming Soon)*

### Week 3: Services, Actions & Lifecycle
- Chapter 5: ROS 2 Services and Actions *(Coming Soon)*
- Chapter 6: Lifecycle Nodes *(Coming Soon)*

### Week 4: Transforms & Robot Models
- Chapter 7: Coordinate Transforms (tf2) *(Coming Soon)*
- Chapter 8: URDF Robot Descriptions *(Coming Soon)*

### Week 5: Testing & CI/CD
- Chapter 9: Unit Testing with pytest *(Coming Soon)*
- Chapter 10: Launch Testing *(Coming Soon)*

---

**Ready to begin?** Start with [Chapter 1: Introduction to Physical AI](./week-1/ch01-physical-ai-intro.mdx) →
