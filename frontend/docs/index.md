---
id: index
title: Physical AI & Humanoid Robotics
description: A Simulation-First Guide to ROS 2 and Vision-Language-Action Systems
---

# Physical AI & Humanoid Robotics

## A Simulation-First Guide to ROS 2 and Vision-Language-Action Systems

Welcome to the **Physical AI & Humanoid Robotics** textbook—a comprehensive 13-week curriculum designed to take you from foundational concepts to deploying advanced robotics systems. Whether you're learning on a laptop, building edge AI solutions on Jetson hardware, or programming physical humanoid robots, this curriculum meets you where you are.

---

## 🎯 What You'll Learn

This textbook bridges the gap between **simulation** and **real-world robotics deployment** through a structured, tier-based learning approach:

- **ROS 2 Fundamentals**: Nodes, topics, services, actions, and the publish-subscribe architecture
- **Simulation Environments**: Gazebo, Isaac Sim, and digital twin concepts for risk-free experimentation
- **Navigation Systems**: SLAM, Nav2, sensor fusion, and autonomous path planning
- **Vision-Language-Action (VLA)**: Multimodal AI models that enable robots to understand and execute natural language commands
- **Edge AI Deployment**: Optimizing models for Jetson hardware with TensorRT and hardware acceleration
- **Physical Robot Integration**: Deploying on Unitree humanoid robots with safety-first practices

---

## 🚀 Three-Tier Learning Path

This curriculum follows the **Three-Tier Imperative**, ensuring accessibility for all learners:

### 🟢 Tier A: Simulation (Required)
**Hardware**: Any laptop with CPU (no GPU required)
**Environment**: ROS 2 Humble, Gazebo, Python simulations
**Goal**: Master concepts through accessible, risk-free simulation

All 4 modules include complete Tier A content. You can complete the entire curriculum using only simulation—no specialized hardware needed.

### 🔵 Tier B: Edge AI (Optional)
**Hardware**: NVIDIA Jetson Orin Nano or Orin NX
**Environment**: Real sensors (cameras, LiDAR, IMU), Isaac Sim, TensorRT
**Goal**: Deploy AI models on edge devices with hardware acceleration

Tier B extends your learning with real sensor integration, edge deployment, and performance optimization.

### 🟣 Tier C: Physical Robot (Optional)
**Hardware**: Unitree Go2 or Unitree G1 humanoid robots
**Environment**: Physical hardware with safety protocols (Dead Man Switch, emergency stops)
**Goal**: Deploy complete systems on physical robots in controlled environments

Tier C represents the full robotics stack—from voice commands to physical locomotion—with rigorous safety requirements.

---

## 📚 Curriculum Structure (13 Weeks)

### Module 1: Foundations of Physical AI (Weeks 1-5)
**Outcome**: Build and test your first ROS 2 robot in simulation

Learn the fundamentals of ROS 2 architecture, Python programming for robotics, and Digital Signal Processing (DSP) concepts. By the end of Module 1, you'll create nodes, publish sensor data, and understand the computational foundations of robotics.

- **Week 1**: Physical AI paradigm and ROS 2 nodes/topics
- **Week 2**: Python for robotics and DSP basics
- **Week 3**: ROS 2 services, actions, and lifecycle management
- **Week 4**: Transforms (tf2), URDF robot models, and coordinate frames
- **Week 5**: Testing frameworks (pytest, launch testing) and CI/CD

**Tier A**: CPU-only simulations with rclpy examples
**Tier B**: Deploy ROS 2 on Jetson with real sensor streams
**Tier C**: URDF models for Unitree robots with hardware integration

---

### Module 2: Simulation & Digital Twins (Weeks 6-7)
**Outcome**: Create realistic robot simulations for rapid iteration

Master Gazebo and Isaac Sim to build digital twins—virtual replicas of physical robots that enable risk-free experimentation and parallel development.

- **Week 6**: Gazebo fundamentals and sensor simulation
- **Week 7**: Isaac Sim, GPU-accelerated physics, and Sim2Real transfer

**Tier A**: Gazebo on CPU with lightweight physics
**Tier B**: Isaac Sim with GPU acceleration and photorealistic rendering
**Tier C**: High-fidelity digital twins matching physical robot parameters

---

### Module 3: Navigation & Embodied AI (Weeks 8-10)
**Outcome**: Deploy voice-to-navigation pipelines using Nav2 and VSLAM

Build autonomous navigation systems using SLAM (Simultaneous Localization and Mapping), sensor fusion, and modern AI techniques like Visual SLAM.

- **Week 8**: Isaac Sim navigation concepts and Nav2 stack
- **Week 9**: SLAM algorithms (GMapping, Cartographer, RTAB-Map)
- **Week 10**: Sensor fusion and voice-controlled navigation

**Tier A**: Nav2 in Gazebo with 2D LiDAR simulation
**Tier B**: Nav2 on Jetson with real LiDAR and depth cameras
**Tier C**: VSLAM deployment on Unitree robots with visual odometry

---

### Module 4: Vision-Language-Action Systems (Weeks 11-13)
**Outcome**: Deploy a VLA model that interprets natural language and controls robot actions

Integrate cutting-edge multimodal AI (OpenVLA, RT-2) to enable robots to understand human language and execute complex manipulation and navigation tasks.

- **Week 11**: VLA architecture and transformer models
- **Week 12**: Fine-tuning VLA models and action space design
- **Week 13**: Capstone project—voice-to-action pipeline

**Tier A**: Run inference on pre-trained VLA models (CPU/GPU)
**Tier B**: TensorRT optimization for real-time inference on Jetson
**Tier C**: Full deployment on Unitree with voice → navigation → manipulation

---

## 🛠️ How to Use This Textbook

### For Self-Learners
1. **Start with Tier A**: Complete all modules using only simulation (no hardware purchase required)
2. **Check Prerequisites**: Each chapter lists required prior knowledge—review earlier material as needed
3. **Complete Quizzes**: Achieve 70% passing score to validate understanding before progressing
4. **Try Exercises**: Hands-on exercises reinforce concepts with acceptance criteria for self-assessment

### For Instructors
- **Modular Structure**: Adapt modules to semester schedules (use Weeks 1-10 for a single semester, or split into two courses)
- **Tiered Assignments**: Assign Tier A exercises to all students; offer Tier B/C as optional challenges or capstone projects
- **Assessment Tools**: Built-in quizzes, reflection questions, and capstone rubrics
- **Hardware Flexibility**: Entire curriculum deliverable without physical hardware

### For Researchers & Practitioners
- **Skip to Your Tier**: If you already have hardware, jump directly to Tier B/C content
- **Architectural Patterns**: Use Mermaid diagrams for ROS 2 graph architectures in your own projects
- **Safety Protocols**: Reference Tier C safety patterns (Dead Man Switch, emergency stops) for production systems

---

## ✅ Prerequisites

- **Programming**: Python fundamentals (variables, functions, classes, file I/O)
- **Math**: Linear algebra (vectors, matrices), basic calculus (derivatives)
- **Terminal**: Command-line navigation, environment variables, package managers
- **Optional**: Docker basics (helpful for ROS 2 containerized workflows)

If you need to review, see the [Prerequisites Guide](./resources/prerequisites.md) for recommended resources.

---

## 📖 Learning Features

### Interactive Components
- **🧪 Exercises**: Hands-on coding challenges with tier-specific variants
- **📝 Quizzes**: Knowledge checks with 70% pass threshold and immediate feedback
- **📋 Prerequisites**: Expandable checklists for each chapter
- **🎨 Mermaid Diagrams**: Interactive ROS 2 graph visualizations

### Pedagogical Structure
Each chapter follows a consistent flow:
1. **Analogy**: Real-world comparison to introduce complex concepts
2. **Concept**: Technical explanation with definitions
3. **Diagram**: Visual representation of architecture or data flow
4. **Example**: Runnable code with explanations
5. **Exercise**: Hands-on practice with acceptance criteria
6. **Summary**: Key takeaways and connections to later modules
7. **Quiz**: Validate understanding before progressing

### Safety-First Design
- **⚠️ Danger Admonitions**: Highlighted safety warnings for Tier B/C hardware operations
- **Dead Man Switch Patterns**: 100ms timeout examples for motor control
- **Emergency Stop Protocols**: Required safety measures for physical robot deployment

---

## 🚀 Get Started

Ready to begin? Choose your path:

- **Module 1: Foundations** → Start here if you're new to ROS 2 or robotics
- **Module 2: Simulation** → Jump here if you're comfortable with ROS 2 basics and want to build digital twins
- **Module 3: Navigation** → Begin here if you're ready to implement SLAM and autonomous navigation
- **Module 4: VLA Systems** → Advanced learners integrating AI with robotics

**Next Steps**:
1. Set up your development environment: [Quickstart Guide](../specs/001-robotics-textbook/quickstart.md)
2. Review the [Hardware Tiers Guide](./resources/hardware-tiers.md) to understand equipment options
3. Dive into [Module 1: Foundations](./module-1/index.md)

---

## 📚 Additional Resources

- **[Glossary](./resources/glossary.md)**: Robotics terminology and acronyms
- **[Hardware Tiers](./resources/hardware-tiers.md)**: Detailed equipment requirements for each tier
- **[ROS 2 Setup](./resources/ros2-setup.md)**: Installation guides for Ubuntu, Windows, macOS
- **[Troubleshooting](./resources/troubleshooting.md)**: Common issues and solutions

---

## 🤝 Contributing

This textbook is an evolving resource. Found an error or have suggestions? See the [Contributing Guide](../CONTRIBUTING.md) for how to submit issues or improvements.

---

## 📄 License

This work is licensed under [MIT License](../LICENSE). Code examples are freely reusable with attribution.

---

**Let's build the future of robotics—starting in simulation, scaling to the real world.** 🤖
