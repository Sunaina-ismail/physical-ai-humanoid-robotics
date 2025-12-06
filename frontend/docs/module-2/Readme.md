---
id: module-2
title: "Module 2: Simulation & Digital Twins"
description: "Weeks 7-7 Content | Tier Support: 🟢 A • 🔵 B • 🟣 C"
---

# Module 2: Simulation & Digital Twins

**Duration**: Weeks 6-7 | **Tier Support**: 🟢 A • 🔵 B • 🟣 C

## Learning Outcome

By the end of Module 2, you will **create realistic robot simulations for rapid iteration**, mastering Gazebo and Isaac Sim to build digital twins—virtual replicas of physical robots that enable risk-free experimentation and parallel development.

---

## Overview

Module 2 teaches the **simulation-first development paradigm** that powers modern robotics engineering. Instead of debugging directly on expensive hardware, you'll learn to:

- **Build digital twins** that mirror physical robot behavior with high fidelity
- **Accelerate development** by testing 100+ scenarios in simulation before hardware deployment
- **Master Gazebo** for CPU-friendly, open-source robotics simulation
- **Leverage Isaac Sim** for GPU-accelerated, photorealistic environments
- **Bridge Sim2Real** by understanding domain randomization and transfer learning

Whether you're prototyping a new robot design, testing navigation algorithms, or training AI models, simulation is your force multiplier.

---

## Why This Module Matters

**Real-world robotics development is expensive and slow**:
- Physical robots cost $1,000–$100,000+
- Hardware failures require repairs and downtime
- Testing dangerous scenarios (obstacle collisions, edge cases) risks equipment damage
- Iteration cycles are limited by access to hardware

**Simulation changes the game**:
- **0-cost experimentation**: Test unlimited scenarios without hardware wear
- **Parallel testing**: Run 10 simulations simultaneously on cloud GPUs
- **Reproducibility**: Exact same conditions for every test run
- **Safety**: Explore edge cases (high-speed collisions, sensor failures) without risk

Companies like **Tesla, Waymo, and Boston Dynamics** develop 80%+ of their robotics stack in simulation before touching hardware. This module teaches you those same workflows.

---

## Week-by-Week Breakdown

### Week 6: Gazebo Fundamentals & Sensor Simulation
**Chapters**:
- Chapter 11: Gazebo Architecture and Physics Engines
- [Chapter 11: Digital Twins and Simulation](./week-6/ch11-digital-twins.mdx) *(Updated Title)*
- Chapter 12: Simulating Sensors (LiDAR, Cameras, IMU)

**Key Concepts**:
- Gazebo Classic vs. Gazebo Sim (formerly Ignition)
- Physics engines (ODE, Bullet, DART) and choosing the right one
- World files (.sdf) and spawning models programmatically
- Sensor plugins (ray sensors for LiDAR, camera sensors, contact sensors)
- Simulated time vs. real-time factor

**Tier A**: Run Gazebo on CPU with basic physics (ODE engine)
**Tier B**: Use GPU ray tracing for LiDAR in Isaac Sim (preview)
**Tier C**: Validate simulation accuracy against real Unitree sensor data

**Milestone**: Build a Gazebo world with obstacles, spawn a robot with LiDAR + camera, and visualize sensor data in RViz

---

### Week 7: Isaac Sim & Sim2Real Transfer
**Chapters**:
- Chapter 13: NVIDIA Isaac Sim Essentials
- Chapter 14: GPU-Accelerated Physics and Rendering
- Chapter 15: Domain Randomization for Sim2Real

**Key Concepts**:
- Isaac Sim architecture (Omniverse, PhysX 5, RTX rendering)
- Importing URDF/USD assets
- GPU-accelerated physics for faster-than-real-time simulation
- Photorealistic rendering for vision model training
- Domain randomization (lighting, textures, physics) to improve real-world transfer

**Tier A**: Run Isaac Sim on gaming GPU (RTX 3060+ or cloud instance)
**Tier B**: Train vision models with Isaac Sim synthetic data, deploy on Jetson
**Tier C**: Create high-fidelity digital twin of Unitree robot with calibrated parameters

**Milestone**: Run a navigation policy trained in Isaac Sim and deploy it to Gazebo or Tier B/C hardware (preview of Module 3)

---

## Three-Tier Learning Path

### 🟢 Tier A: Simulation on CPU/GPU (Required)
**Hardware**: Laptop or desktop with Ubuntu 22.04 (or Docker)
**Software**: Gazebo Classic 11 or Gazebo Sim (Fortress/Garden), ROS 2 Humble

Tier A focuses on **Gazebo**, which runs on modest hardware:
- CPU-only physics simulation (sufficient for most robotics tasks)
- 2D LiDAR and RGB cameras
- Basic physics (rigid body dynamics, collision detection)

**When to use Isaac Sim (Tier A)**: If you have a gaming GPU (RTX 3060+) or cloud access, you can optionally explore Isaac Sim basics at the end of Week 7.

**Recommended**: Start with Gazebo Classic for simplicity, then try Gazebo Sim (newer architecture) in Week 6.

---

### 🔵 Tier B: Isaac Sim + Jetson Integration (Optional Extension)
**Hardware**: NVIDIA GPU (RTX 3060+, A100, or cloud instance) + Jetson Orin for deployment
**Software**: Isaac Sim 2023.1+, ROS 2 bridge, TensorRT

Tier B adds:
- **GPU ray tracing** for photorealistic LiDAR and camera simulation
- **Synthetic data generation** for training vision models
- **Sim-to-Jetson workflows**: Train in Isaac Sim, deploy on Jetson with TensorRT
- **Faster-than-real-time simulation** (10x-100x with GPU physics)

**Use case**: Training perception models (object detection, segmentation) with synthetic data before deploying to Tier B hardware.

---

### 🟣 Tier C: High-Fidelity Digital Twins (Optional Extension)
**Hardware**: Unitree Go2 or G1 + access to Isaac Sim or Gazebo
**Software**: Unitree URDF models, calibrated physics parameters

Tier C adds:
- **Parameter calibration**: Match simulation physics (friction, damping, motor torque) to real robot measurements
- **Validation workflows**: Test policies in simulation, then verify on hardware
- **Digital twin monitoring**: Run simulation alongside physical robot to predict failures

**Use case**: Before deploying a new navigation policy to your $16,000 Unitree G1, test it in a calibrated digital twin to catch edge cases.

**⚠️ Safety Note**: Even with high-fidelity simulation, always test cautiously on physical hardware. Sim2Real gap is never zero.

---

## Prerequisites

Before starting Module 2, you should have completed:

- **Module 1 (Weeks 1-4)**: ROS 2 fundamentals, URDF modeling, tf2 transforms
- **Comfort with RViz**: Visualizing sensor data and robot models
- **Linux CLI**: Installing packages, running launch files

**Helpful (Not Required)**:
- GPU experience (for Isaac Sim in Week 7)
- 3D modeling basics (for custom robot designs)

**Checkpoint**: Can you create a URDF robot with a camera and visualize it in Gazebo? If yes, you're ready.

---

## Learning Resources

### Official Documentation
- [Gazebo Sim Docs](https://gazebosim.org/docs) (newest version)
- [Gazebo Classic Tutorials](http://classic.gazebosim.org/tutorials)
- [Isaac Sim Documentation](https://docs.omniverse.nvidia.com/app_isaacsim/app_isaacsim/overview.html)
- [ROS 2 Gazebo Integration](https://github.com/ros-simulation/gazebo_ros_pkgs)

### Key Concepts
- **Digital Twin**: A virtual model that continuously updates based on real-world data
- **Sim2Real Gap**: Differences between simulation and reality (physics inaccuracies, sensor noise)
- **Domain Randomization**: Varying simulation parameters (lighting, textures) to make models robust to real-world variability
- **Real-Time Factor (RTF)**: Simulation speed relative to real time (RTF=2.0 means 2x faster than reality)

### Community Resources
- [Gazebo Community](https://community.gazebosim.org/)
- [NVIDIA Omniverse Forum](https://forums.developer.nvidia.com/c/omniverse/)
- [r/ROS Simulation Discussions](https://reddit.com/r/ROS)

---

## Assessment & Progression

### Knowledge Checks
- **Quizzes**: 70% passing threshold for each chapter
- **Hands-On Exercises**:
  - Week 6: Build a custom Gazebo world with dynamic obstacles
  - Week 7: Generate synthetic camera data in Isaac Sim
- **Capstone Preview**: Create a digital twin of a custom robot design

### How to Know You're Ready for Module 3
You should be able to:
1. ✅ Spawn robots and sensors in Gazebo using launch files
2. ✅ Explain trade-offs between Gazebo (CPU-friendly) and Isaac Sim (GPU-accelerated)
3. ✅ Visualize simulated LiDAR and camera data in RViz
4. ✅ Understand the Sim2Real gap and how domain randomization helps
5. ✅ (Tier B/C) Run a basic Isaac Sim scenario and export sensor data

If you can confidently simulate a robot navigating an obstacle course in Gazebo or Isaac Sim, you're ready for **Module 3: Navigation & Embodied AI**.

---

## What's Next?

After completing Module 2:
- **Module 3** uses your simulation skills to develop SLAM and Nav2 navigation stacks
- **Module 4** trains Vision-Language-Action models using synthetic data from Isaac Sim

**Why simulation matters for navigation**: You'll test SLAM algorithms in 100+ simulated environments (small rooms, warehouses, outdoor spaces) before ever needing a physical robot.

**Start Learning**: Proceed to [Chapter 11: Digital Twins and Simulation](./week-6/ch11-digital-twins.mdx)

---

## Chapter List

### Week 6: Gazebo Fundamentals
- [Chapter 11: Digital Twins and Simulation](./week-6/ch11-digital-twins.mdx)
- Chapter 12: Simulating Sensors (LiDAR, Cameras, IMU) *(Coming Soon)*

### Week 7: Isaac Sim & Sim2Real
- Chapter 13: NVIDIA Isaac Sim Essentials *(Coming Soon)*
- Chapter 14: GPU-Accelerated Physics *(Coming Soon)*
- Chapter 15: Domain Randomization *(Coming Soon)*

---

**Ready to build your first digital twin?** Start with [Chapter 11: Digital Twins and Simulation](./week-6/ch11-digital-twins.mdx) →
