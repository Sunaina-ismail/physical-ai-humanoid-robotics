# Hardware Tiers Reference

**Complete guide to the Three-Tier learning system: Simulation → Edge AI → Physical Robot**

---

## Overview: The Three-Tier Imperative

This textbook uses a **progressive hardware approach** that prioritizes accessibility while enabling advanced learners to deploy to real robots. Every chapter provides **Tier A (Simulation)** content as the foundation, with optional **Tier B (Edge AI)** and **Tier C (Physical Robot)** extensions.

### Why Three Tiers?

1. **Accessibility**: Tier A requires only a laptop—no GPU, no expensive hardware, no safety concerns
2. **Scalability**: Learners progress at their own pace based on available resources
3. **Safety**: Test in simulation before deploying to hardware that can cause injury or property damage
4. **Cost-effectiveness**: Invest in hardware only after validating skills in simulation
5. **Industry alignment**: Sim-to-real workflow mirrors professional robotics development

---

## Tier A: Simulation-Only (CPU) 🟢

**Target Audience**: Beginners, students, anyone with a laptop

### Hardware Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| **CPU** | Intel i5 / Ryzen 5 (4 cores) | Intel i7 / Ryzen 7 (8 cores) |
| **RAM** | 8 GB | 16 GB |
| **Storage** | 50 GB free | 100 GB SSD |
| **GPU** | None required | None required (CPU-only) |
| **OS** | Ubuntu 22.04 LTS | Ubuntu 22.04 LTS |

### Software Stack

- **ROS 2 Humble**: Middleware and robotics libraries
- **Gazebo Classic or Gazebo Fortress**: Physics-based 3D simulation
- **Python 3.10+**: Primary programming language (rclpy)
- **rqt Tools**: Visualization, plotting, introspection
- **OpenCV (CPU)**: Computer vision (feature detection, image processing)

### What You Can Do

✅ **All core robotics concepts**:
- ROS 2 nodes, topics, services, actions
- Robot kinematics and URDF modeling
- Sensor simulation (cameras, LiDAR, IMU)
- Path planning and navigation (Nav2)
- Basic computer vision (color detection, blob tracking)
- State machines and behavior trees
- Multi-robot simulation

✅ **Capstone Project (Tier A variant)**:
- Voice-to-navigation pipeline in Gazebo
- Simulated Whisper speech recognition (pre-recorded commands)
- LLM-based task planning (GPT API or local Llama)
- Nav2 autonomous navigation in simulated warehouse
- Conceptual design of manipulation tasks

### Limitations

❌ **No GPU acceleration**: Deep learning inference is slow (1-5 FPS for YOLO, semantic segmentation)
❌ **Simulation-reality gap**: Physics, sensor noise, and lighting don't perfectly match real world
❌ **No tactile feedback**: Cannot simulate force sensors, compliance, or physical interactions accurately

### Cost

**$0 - $800** (laptop cost only; software is free and open-source)

---

## Tier B: Edge AI (Jetson Orin) 🔵

**Target Audience**: Intermediate learners, hobbyists, edge AI enthusiasts

### Hardware Requirements

| Component | Specification | Cost (USD) |
|-----------|---------------|------------|
| **Jetson Orin Nano** | 8GB RAM, 1024 CUDA cores, 40 TOPS | $499 |
| **Jetson Orin NX** | 16GB RAM, 1024 CUDA cores, 100 TOPS | $699 |
| **Power Supply** | USB-C PD (15W - 25W) | $30 |
| **Storage** | NVMe SSD (256GB+) | $50 |
| **Development Kit** | Carrier board, cooling, I/O | Included |
| **RealSense D435i** | RGB-D camera (depth + color) | $329 |
| **Hokuyo UST-10LX** | 2D LiDAR (270°, 10m range) | $1,200 |
| **(Optional) IMU** | Bosch BNO055 or Xsens MTi-3 | $50 - $500 |

**Total Cost**: ~$1,800 - $3,000 (Orin Nano setup) | ~$2,000 - $3,500 (Orin NX setup)

### Software Stack

- **JetPack 6.x**: NVIDIA's Linux OS with GPU drivers, CUDA, TensorRT
- **ROS 2 Humble**: Native ARM64 support
- **TensorRT**: GPU-accelerated deep learning inference (YOLOv8, SegFormer)
- **Isaac ROS**: NVIDIA's hardware-accelerated ROS 2 packages (AprilTags, VSLAM, DNN inference)
- **PyTorch / TensorFlow**: Deep learning frameworks with CUDA support
- **OpenCV (CUDA)**: GPU-accelerated computer vision

### What You Can Do

✅ **Everything in Tier A, plus**:
- **Real-time deep learning**: Object detection (YOLOv8 @ 30 FPS), semantic segmentation, pose estimation
- **VSLAM**: Visual SLAM using stereo or RGB-D cameras (ORB-SLAM3, RTAB-Map)
- **Real sensor integration**: Deploy to wheeled robots, robotic arms, or drones
- **Edge deployment**: Run models on battery-powered mobile platforms
- **Sensor fusion**: Combine camera, LiDAR, IMU for robust perception

✅ **Capstone Project (Tier B variant)**:
- Voice-to-navigation on real wheeled robot (TurtleBot3, custom platform)
- Real Whisper model on Jetson (GPU-accelerated)
- YOLOv8 object detection for obstacle avoidance
- Nav2 with real LiDAR and RGB-D sensors
- Autonomous navigation in real indoor environments

### Limitations

❌ **No legged locomotion**: Wheeled robots only (no humanoid balance control)
❌ **Limited manipulation**: Can control arms but no full humanoid manipulation stacks
❌ **Power constraints**: Battery life limits extended operation (2-4 hours typical)

### Safety Considerations

⚠️ **Moving platforms**: Risk of collision with people, pets, or objects
⚠️ **Sensor hazards**: LiDAR eye safety (Class 1 lasers are safe; Class 3 require warnings)
⚠️ **Battery safety**: LiPo/Li-ion fire risk if damaged or improperly charged

**Required**:
- Emergency stop button (physical kill switch)
- Geofencing (software boundaries to prevent escapes)
- Collision detection and emergency braking
- Supervision during all testing

---

## Tier C: Physical Robot (Unitree H1) 🟣

**Target Audience**: Advanced learners, researchers, robotics professionals

### Hardware Requirements

| Component | Specification | Cost (USD) |
|-----------|---------------|------------|
| **Unitree H1 Humanoid** | 19 DOF, 1.8m height, 47kg weight | $90,000 - $150,000 |
| **Onboard Computer** | NVIDIA Jetson AGX Orin (64GB) | Included |
| **Sensors** | RealSense D435i (head), IMU, force sensors (feet) | Included |
| **Power System** | 48V battery pack, 2-hour runtime | Included |
| **Development Station** | Workstation PC (for remote development) | $2,000 |
| **Safety Equipment** | Crash mats, safety barriers, kill switch | $1,000 |

**Total Cost**: ~$93,000 - $155,000 (plus facility requirements)

### Facility Requirements

- **Space**: Minimum 5m x 5m clear area for locomotion testing
- **Power**: 110V/220V AC for battery charging
- **Flooring**: Non-slip, cushioned surface preferred
- **Lighting**: Good overhead lighting for vision systems
- **Safety**: Emergency stop system, trained personnel

### Software Stack

- **Unitree SDK**: Proprietary control libraries for H1
- **ROS 2 Humble**: Integration layer for custom software
- **Isaac Sim**: Digital twin for H1 (simulation before hardware testing)
- **MoveIt 2**: Motion planning for manipulation tasks
- **Nav2**: Modified for legged locomotion (bipedal walking controllers)
- **VLA Models**: Vision-Language-Action models (RT-2, OpenVLA)

### What You Can Do

✅ **Everything in Tiers A & B, plus**:
- **Humanoid locomotion**: Walking, turning, climbing stairs, dynamic balancing
- **Full-body manipulation**: Coordinated arm + locomotion (walk to object, grasp, carry)
- **Physical human-robot interaction**: Handoffs, following, gesture recognition
- **Real-world deployment**: Warehouse navigation, household assistance, research experiments
- **Multi-modal learning**: Imitation learning from human demonstrations

✅ **Capstone Project (Tier C variant)**:
- Voice-to-action on physical Unitree H1
- Real Whisper + LLM on AGX Orin
- "Go to the kitchen and pick up the red mug" → full execution
- Real VSLAM, Nav2 bipedal navigation, MoveIt grasp planning
- Force-feedback manipulation with safety limits

### Limitations

❌ **High cost**: Requires institutional funding or industry sponsorship
❌ **Maintenance**: Requires mechanical expertise for repairs, calibration
❌ **Specialized knowledge**: Legged locomotion, whole-body control, safety protocols

### Safety Considerations (Critical)

⚠️ **High-risk system**:
- **Physical harm**: 47kg robot can cause serious injury during falls or collisions
- **Crushing hazards**: Joints can apply hundreds of Newtons of force
- **Electrical hazards**: 48V battery system
- **Fall risk**: Robot may fall during balance failures, damaging itself or surroundings

**Mandatory Safety Protocols**:
1. **Dead Man Switch**: 100ms timeout, immediately cuts all motor power
2. **Emergency Stop**: Accessible hardware button within 1 meter of operator
3. **Geofencing**: Absolute software limits on joint angles and end-effector positions
4. **Trained Personnel**: Minimum 40 hours of supervised training before solo operation
5. **Protective Barriers**: Physical barriers during autonomous testing
6. **Insurance**: Liability coverage for robotics research/education

**Never**:
- ❌ Operate without a second person present
- ❌ Allow untrained individuals near active robot
- ❌ Disable safety systems for "debugging"
- ❌ Test untried code directly on hardware (use Tier A/B first)

---

## Tier Comparison Table

| Feature | Tier A 🟢 | Tier B 🔵 | Tier C 🟣 |
|---------|-----------|-----------|-----------|
| **Cost** | $0 - $800 | $1,800 - $3,500 | $93,000+ |
| **Hardware** | Laptop (CPU-only) | Jetson Orin + sensors | Unitree H1 humanoid |
| **Risk** | Zero (simulation) | Low (wheeled robot) | High (full humanoid) |
| **Setup Time** | 2-4 hours | 1-2 days | 1-2 weeks |
| **Deep Learning** | Slow (CPU) | Fast (GPU, 30 FPS) | Fast (AGX Orin) |
| **Locomotion** | Simulated | Wheeled | Bipedal walking |
| **Manipulation** | Simulated | Basic arms | Full dual-arm |
| **Sim-to-Real Gap** | N/A (all sim) | Moderate | High (most challenging) |
| **Supervision** | None required | Recommended | Mandatory |
| **Training Required** | None | Minimal (safety) | Extensive (40+ hours) |

---

## Choosing Your Tier

### Start with Tier A if...
- ✅ You're new to robotics or ROS 2
- ✅ You want to learn concepts without hardware investment
- ✅ You're a student with limited budget
- ✅ You prefer risk-free experimentation

### Add Tier B if...
- ✅ You've completed Modules 1-2 (ROS 2, simulation)
- ✅ You want to deploy real robots or drones
- ✅ You're interested in edge AI and embedded systems
- ✅ You have $2,000-$3,500 for hardware

### Add Tier C if...
- ✅ You've completed the full curriculum (Modules 1-4)
- ✅ You have institutional access to Unitree H1 or similar humanoid
- ✅ You're pursuing robotics research or professional development
- ✅ You have trained safety personnel and proper facilities

---

## Progression Path Recommendations

### Path 1: Academic Learner (Budget-Conscious)
1. **Weeks 1-10**: Complete Modules 1-3 in Tier A (Gazebo)
2. **Weeks 11-13**: Complete Module 4 capstone in Tier A
3. **Optional**: Apply for lab access to Tier C robots at university

### Path 2: Hobbyist / Self-Learner
1. **Weeks 1-5**: Complete Module 1 in Tier A
2. **Weeks 6-7**: Order Jetson Orin Nano + RealSense camera
3. **Weeks 8-10**: Complete Module 2-3 in Tier A, then port to Tier B hardware
4. **Weeks 11-13**: Capstone in Tier B (real wheeled robot)

### Path 3: Professional / Researcher
1. **Weeks 1-7**: Speed-run Modules 1-2 in Tier A (1 week each)
2. **Weeks 8-10**: Module 3 in Tier B (Jetson + sensors)
3. **Weeks 11-13**: Module 4 capstone in Tier C (Unitree H1 access)
4. **Post-course**: Publish research results, contribute to open-source

---

## Tier-Specific Learning Outcomes

### Tier A Graduates Can...
- Design and simulate complete robot systems in Gazebo
- Write production-quality ROS 2 Python code (nodes, topics, services, actions)
- Debug robotics systems using rqt tools and logs
- Understand sensor-action loops, state machines, navigation stacks
- Explain sim-to-real challenges and mitigation strategies

### Tier B Graduates Can...
- Deploy deep learning models on edge hardware (Jetson)
- Integrate real sensors (cameras, LiDAR, IMU) with ROS 2
- Troubleshoot hardware issues (sensor calibration, driver configuration)
- Optimize models for inference speed vs. accuracy
- Navigate real indoor environments autonomously

### Tier C Graduates Can...
- Operate humanoid robots safely under supervision
- Implement whole-body control and legged locomotion
- Debug complex multi-modal systems (vision + speech + manipulation)
- Design fail-safe mechanisms and recovery behaviors
- Conduct robotics research publishable in conferences (ICRA, IROS, RSS)

---

## FAQ

### Can I skip Tier A and go straight to Tier B or C?
**Not recommended.** Tier A provides conceptual foundations, debugging skills, and safety-first mindset. Testing unvalidated code on hardware risks damage and injury. Industry professionals always prototype in simulation first.

### Do I need to complete all three tiers to finish the course?
**No.** Tier A alone provides a complete robotics education. Tiers B and C are optional enrichments for learners with additional resources.

### Can I use different hardware for Tier B (e.g., Raspberry Pi 5)?
**Partial compatibility.** ROS 2 runs on Raspberry Pi, but you won't get GPU acceleration for deep learning. You'll be limited to classical computer vision (OpenCV, feature detection) and lightweight models.

### What if my institution has a different humanoid robot (not Unitree H1)?
**Adaptable.** The concepts apply to any humanoid platform (Boston Dynamics Atlas, Figure 02, Sanctuary AI Phoenix). You'll need platform-specific SDK knowledge, but ROS 2 integration patterns are universal.

### How much does it cost to run the Tier A curriculum?
**$0** if you have a laptop. All software (ROS 2, Gazebo, Python libraries) is free and open-source.

---

## Further Resources

### Tier A (Simulation)
- [Gazebo Tutorials](https://gazebosim.org/docs) - Official simulation guides
- [ROS 2 Humble Documentation](https://docs.ros.org/en/humble/) - Complete API reference
- [The Construct Sim](https://www.theconstructsim.com/) - Cloud-based ROS 2 simulation

### Tier B (Edge AI)
- [NVIDIA Jetson Docs](https://developer.nvidia.com/embedded-computing) - JetPack, Isaac ROS
- [Intel RealSense SDK](https://github.com/IntelRealSense/librealsense) - Camera integration
- [TensorRT Developer Guide](https://docs.nvidia.com/deeplearning/tensorrt/) - GPU inference optimization

### Tier C (Physical Robot)
- [Unitree Robotics SDK](https://github.com/unitreerobotics) - H1 control libraries
- [MoveIt 2 Tutorials](https://moveit.picknik.ai/humble/index.html) - Motion planning
- [Safety Standards (ISO 10218)](https://www.iso.org/standard/51330.html) - Industrial robot safety

---

**Last Updated**: 2025-12-05
**License**: CC BY-SA 4.0
