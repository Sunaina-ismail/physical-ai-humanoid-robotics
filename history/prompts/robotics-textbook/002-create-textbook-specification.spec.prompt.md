---
id: 002
title: Create Physical AI Robotics Textbook Specification
stage: spec
date: 2025-12-04
surface: agent
model: claude-sonnet-4-5-20250929
feature: robotics-textbook
branch: 001-robotics-textbook
user: CBM
command: /sp.specify
labels: ["specification", "physical-ai", "robotics", "education", "docusaurus"]
links:
  spec: specs/001-robotics-textbook/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/001-robotics-textbook/spec.md
  - specs/001-robotics-textbook/checklists/requirements.md
tests:
  - Specification quality validation checklist (all items passed)
---

## Prompt

# Product Specification: Physical AI & Humanoid Robotics Textbook
## 1. Overview
The goal is to build a comprehensive, open-source, beginner-friendly yet industry-aligned technical textbook titled:

**"Physical AI & Humanoid Robotics: A Simulation-First Guide"**

This book converts the 13-week curriculum into a **fully structured Docusaurus-powered learning platform** that enables absolute beginners to learn the full pipeline of Physical AI — from sensors and ROS 2 to Isaac Sim, VSLAM, Nav2, and Vision-Language-Action robotics.

**Core Promise:**
> "Learn to control humanoid robots using ROS 2 and Isaac Sim — even if you only have a laptop."

The book must serve as both **theoretical grounding** and **practical simulation-driven learning**, with fallback paths for students without high-end hardware.

---
## 2. User Personas (Readers)
### **Tier A — The Student (Simulation-Only)**
- Has only a laptop (no robot, no GPU).
- Relies entirely on Isaac Sim conceptual flows, Gazebo CPU simulations, Mermaid diagrams, and theoretical understanding.
- Needs conceptual mastery + CPU-friendly examples.

### **Tier B — The Maker (Edge AI Developer)**
- Owns a Jetson Nano or Orin.
- Wants real-world robotics deployment.
- Uses book's "physical deployment" extension sections.

### **Tier C — The Researcher (Advanced Hardware)**
- Has access to Unitree Go2/G1 or similar humanoids.
- Needs Sim-to-Real transfers, Nav2 mapping, VSLAM pipelines, hardware integration theory.

---
## 3. Functional Requirements (Course Syllabus → Book Structure)

The book must fully cover the **13-week official course** across **4 Modules**.
---

### **Module 1 — The Robotic Nervous System**
**Weeks 1–5 (Foundations of Physical AI)**
- What is Physical AI, embodied intelligence, and humanoids
- Popular systems used today (ChatGPT → real-world robots, Tesla Optimus, Figure 02, Boston Dynamics)
- ROS 2 Humble Basics
  - Nodes, Topics, Services, Actions
  - Message passing, TF Frames, Launch files
- Python (`rclpy`) fundamentals
- URDF for humanoid robot models
- Sensors & Actuators (camera, IMU, lidar, servos)
- Safety & Control Theory (Dead-Man Switch)

**Outcome:** Students understand **how robots "think," perceive, and move**.

---

### **Module 2 — The Digital Twin**
**Weeks 6–7 (Simulation Foundations)**
- What is a Digital Twin? Why simulation-first?
- Gazebo physics fundamentals
- URDF vs SDF
- CPU-only simulation fallback for Tier A
- Sensor simulation (Depth, LiDAR, IMU)
- Unity for high-fidelity visualization and HRI demos

**Outcome:** Students can **simulate robot bodies, sensors, and environments**.

---

### **Module 3 — The AI-Robot Brain**
**Weeks 8–10 (Perception → Planning → Control)**
- NVIDIA Isaac Sim (conceptual pipelines only)
- Synthetic data generation
- VSLAM: mapping, landmarks, pose estimation
- Nav2: global/local planning, costmaps, planners, controllers
- Sim-to-Real challenges (domain randomization, calibration concepts)

**Outcome:** Students understand **how robots localize, map, and plan paths**.

---

### **Module 4 — Vision-Language-Action**
**Weeks 11–13 (Robotics + LLM + Voice)**
- Whisper pipeline (Speech → Text)
- LLM Planning (Intent → ROS Actions)
- VLA Architectures
  - Perception grounding
  - Skill graphs
  - LLM-to-Action Policies
- Capstone Project:
  **"Autonomous Humanoid: Voice → Plan → Navigate → Interact"**
  - Only conceptual implementation
  - Full simulation allowed
  - Hardware optional (Tier B/C)

**Outcome:** Students understand **robot intelligence driven by voice + LLMs**.

---

## 4. Non-Functional Requirements

### **4.1 Writing Standards**
- Start every lesson with:
  **Analogy → Concept → Diagram → Example → Exercise → Summary → Quiz**
- No OS-level install instructions unless inside Tier B/C hardware sections.
- All explanations must be beginner-friendly.

### **4.2 Pedagogical Best Practices**
- Each chapter begins with measurable **Learning Outcomes** (Bloom's Taxonomy).
- Add **Prerequisite Knowledge** for each lesson.
- Add **Reflection Questions** at the end.
- Include teaching scaffolds:
  - "Before you learn this…"
  - "Common misunderstanding…"
  - "Real-world analogy…"

### **4.3 Mermaid-Only Diagrams**
All system, architecture, ROS graph, VLA, Nav2, TF, and data-flow diagrams must be rendered using **Mermaid.js**, including alt-text descriptions.

### **4.4 Simulation-First Requirement**
Every lab must include a **Tier A (CPU-only)** fallback.

## 6. Success Metrics

- Completeness: 13 weeks of content fully generated as 4 modules.
- Pedagogical Quality: Each chapter uses template + Bloom learning outcomes.
- Beginner Accessibility: Tier A must be able to finish the whole book with only a laptop.
- Professional Rigor: Reflects ROS 2, Gazebo, Isaac, Nav2, Whisper, and VLA concepts correctly.

## Response snapshot

Created comprehensive specification for Physical AI & Humanoid Robotics textbook following Spec-Driven Development workflow:

**Branch & Structure Created**:
- Created feature branch: `001-robotics-textbook`
- Initialized spec directory: `specs/001-robotics-textbook/`

**Specification Developed** (specs/001-robotics-textbook/spec.md):
- **4 User Stories** with priority-based learning paths:
  - P1: Complete Beginner Path (Tier A - laptop-only)
  - P2: Edge AI Developer Path (Tier B - Jetson hardware)
  - P3: Advanced Researcher Path (Tier C - humanoid hardware)
  - P1: Self-Paced Pedagogical Scaffolding (cross-cutting)
- **20 Functional Requirements** covering:
  - 4-module curriculum structure (13 weeks)
  - Pedagogical template (Analogy → Concept → Diagram → Example → Exercise → Summary → Quiz)
  - Tier-based accessibility (A/B/C hardware paths)
  - Mermaid.js diagram requirements
  - Docusaurus platform delivery
- **7 Key Entities**: Module, Chapter, Learning Tier, Exercise/Lab, Diagram, Quiz, Capstone Project
- **15 Success Criteria** with measurable outcomes (100% template adherence, 90% prerequisite identification, 85% quiz pass rate)
- **6 Edge Cases** addressing hardware limitations, OS compatibility, accessibility
- **Dependencies, Constraints, Assumptions** sections fully documented
- **Out of Scope** section with 12 explicit exclusions

**Quality Validation** (specs/001-robotics-textbook/checklists/requirements.md):
- Created validation checklist with 14 quality criteria
- All items **PASSED**:
  - No implementation details in requirements
  - All requirements testable and unambiguous
  - Success criteria measurable and technology-agnostic
  - Zero [NEEDS CLARIFICATION] markers (all requirements fully specified)
  - All mandatory sections complete
- **Specification ready for `/sp.clarify` or `/sp.plan`**

**Key Design Decisions**:
- Made informed assumptions about hardware (modest laptop for Tier A, Jetson ~$100-500 for Tier B, institutional access for Tier C)
- Assumed static quiz implementation (no backend grading) suitable for MVP
- Assumed Mermaid.js sufficient for all technical diagrams
- Documented all assumptions explicitly in spec
- No clarification questions needed - all ambiguities resolved through reasonable defaults

## Outcome

- ✅ Impact: Complete, validated specification for comprehensive robotics textbook covering 13-week curriculum with 4 modules, tier-based accessibility, and pedagogical scaffolding
- 🧪 Tests: Specification quality checklist validation (14/14 items passed)
- 📁 Files: 2 files created (spec.md, requirements.md checklist)
- 🔁 Next prompts: `/sp.plan` to design implementation architecture, or `/sp.clarify` if user wants to refine requirements
- 🧠 Reflection: Successfully created specification without needing user clarifications by making informed assumptions and documenting them explicitly. Strong focus on Tier A (laptop-only) accessibility aligns with "simulation-first" promise. Pedagogical structure is well-defined and measurable.

## Evaluation notes (flywheel)

- Failure modes observed: None - spec creation followed workflow cleanly
- Graders run and results (PASS/FAIL): Specification quality checklist - PASS (14/14 items)
- Prompt variant (if applicable): Standard /sp.specify workflow
- Next experiment (smallest change to try): Consider creating a chapter template document to further standardize the pedagogical structure implementation
