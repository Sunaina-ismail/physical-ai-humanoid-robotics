# Tasks: Physical AI & Humanoid Robotics Textbook

**Branch**: `001-robotics-textbook` | **Spec**: [spec.md](./spec.md) | **Plan**: [plan.md](./plan.md)

## Implementation Strategy

**MVP Scope**: Phases 1-8 (38 tasks) - Complete beginner learning path with representative chapters and all tier extensions
**Full Curriculum Scope**: Phases 1-9 (61 tasks) - All 13 weeks with comprehensive chapter coverage
**Incremental Delivery**: Setup → Foundation → US1 (MVP) → US4 → US2 → US3 → Polish → Complete Curriculum

**Total Tasks**: 61
**MVP Tasks**: 38 (completed)
**Remaining Tasks**: 8 (Phase 9)
**Parallelizable**: 47 (77%)

---

## Phase 1: Setup (4 tasks) ✅ COMPLETE

**Goal**: Initialize Docusaurus project and folder structure

- [X] T001 Create `frontend/` directory and run `npx create-docusaurus@latest frontend classic --typescript`
- [X] T002 Install dependencies: `npm install @docusaurus/theme-mermaid` and `npm install -D prettier playwright @axe-core/playwright jest`
- [X] T003 Create folder structure: `frontend/docs/module-{1,2,3,4}`, `frontend/src/components/`, `tests/{e2e,content,code-examples}/`
- [X] T004 Configure `frontend/docusaurus.config.ts` with Mermaid plugin and `frontend/sidebars.ts` with 4-module structure

---

## Phase 2: Foundational Components (6 tasks) ✅ COMPLETE

**Goal**: Build reusable React components for all chapters

- [X] T005 [P] Create `frontend/src/components/TierBadge.tsx` with A/B/C tier indicators per `contracts/`
- [X] T006 [P] Create `frontend/src/components/MermaidDiagram.tsx` with required altText prop per `contracts/mermaid-diagram-props.ts`
- [X] T007 [P] Create `frontend/src/components/CodeExample.tsx` with syntax highlighting
- [X] T008 [P] Create `frontend/src/components/Exercise.tsx` supporting tier variants per `contracts/exercise-props.ts`
- [X] T009 [P] Create `frontend/src/components/Quiz.tsx` with 70% threshold per `contracts/quiz-props.ts`
- [X] T010 [P] Create `frontend/src/components/PrerequisiteCheck.tsx` displaying prerequisites array

---

## Phase 3: User Story 1 - Complete Beginner Path (P1) (10 tasks) ✅ COMPLETE

**Goal**: Tier A (simulation-only) content for all 4 modules

**Test**: Tester with laptop (no GPU) completes Modules 1-4, understands concepts, passes quizzes

- [X] T011 Create `frontend/docs/index.md` landing page with curriculum overview
- [X] T012 [P] [US1] Create `frontend/docs/module-1/index.md` (Foundations, Weeks 1-5)
- [X] T013 [US1] Generate `frontend/docs/module-1/week-1/ch01-physical-ai-intro.mdx` using Curriculum Architect + Technical Writer agents (Tier A: conceptual)
- [X] T014 [US1] Generate `frontend/docs/module-1/week-1/ch02-ros2-nodes-topics.mdx` (Tier A: rclpy examples, CPU-only)
- [X] T015 [P] [US1] Create `frontend/docs/module-2/index.md` (Simulation, Weeks 6-7)
- [X] T016 [US1] Generate `frontend/docs/module-2/week-6/ch11-digital-twins.mdx` (Tier A: Gazebo CPU-only)
- [X] T017 [P] [US1] Create `frontend/docs/module-3/index.md` (Navigation, Weeks 8-10)
- [X] T018 [US1] Generate `frontend/docs/module-3/week-8/ch16-isaac-sim-concepts.mdx` (Tier A: conceptual Mermaid diagrams)
- [X] T019 [P] [US1] Create `frontend/docs/module-4/index.md` (VLA, Weeks 11-13)
- [X] T020 [US1] Generate `frontend/docs/module-4/week-13/ch28-capstone-project.mdx` (Tier A: conceptual design)

---

## Phase 4: User Story 4 - Pedagogical Scaffolding (P1) (5 tasks) ✅ COMPLETE

**Goal**: Add learning outcomes, prerequisites, quizzes to all chapters

**Test**: Learner sees prerequisites, completes quizzes with 70% pass, uses reflection questions

- [X] T021 [P] [US4] Create `tests/content/validate_frontmatter.py` checking schema per `contracts/chapter-frontmatter.yaml`
- [X] T022 [US4] Add frontmatter (learning_outcomes, prerequisites, tier_support) to all Module 1 chapters
- [X] T023 [US4] Add `<Quiz>` components to all Module 1 chapters with hints linking to sections
- [X] T024 [US4] Add frontmatter and quizzes to all Module 2-4 chapters
- [X] T025 [P] [US4] Create `frontend/docs/resources/glossary.md` and `frontend/docs/resources/hardware-tiers.md`

---

## Phase 5: User Story 2 - Edge AI Path (P2) (4 tasks)

**Goal**: Tier B extensions for Jetson deployment

**Test**: Developer with Jetson deploys 3+ robotics examples on edge hardware

- [x] T026 [P] [US2] Add Tier B extension `frontend/docs/module-1/week-2/tierB-jetson-setup.mdx` (ROS 2 on Jetson)
- [x] T027 [P] [US2] Add Tier B extension `frontend/docs/module-2/week-7/tierB-sensor-integration.mdx` (Real sensors)
- [x] T028 [P] [US2] Add Tier B extension `frontend/docs/module-3/week-9/tierB-nav2-edge.mdx` (Nav2 with LiDAR)
- [x] T029 [US2] Add `:::danger` safety admonitions to all Tier B chapters per Constitution IV

---

## Phase 6: User Story 3 - Physical Robot Path (P3) (3 tasks)

**Goal**: Tier C extensions for Unitree humanoid robots

**Test**: Researcher deploys VSLAM on physical robot, achieves voice-to-navigation pipeline

- [X] T030 [P] [US3] Add Tier C extension `frontend/docs/module-3/week-8/tierC-vslam-humanoid.mdx` (VSLAM on Unitree)
- [X] T031 [P] [US3] Add Tier C extension `frontend/docs/module-4/week-13/tierC-full-capstone.mdx` (Physical deployment)
- [X] T032 [US3] Add Dead Man Switch code examples (100ms timeout) to all Tier C motor control chapters

---

## Phase 7: Validation & Testing (4 tasks) ✅ COMPLETE

**Goal**: Ensure quality, accessibility, technical correctness

- [X] T033 [P] Create `tests/content/validate_diagrams.py` checking altText presence
- [X] T034 [P] Create `tests/content/validate_tiers.py` verifying Tier A coverage
- [X] T035 [P] Create `tests/e2e/accessibility.spec.ts` (Playwright + axe-core, keyboard nav)
- [X] T036 Run all tests: `pytest tests/` and `npm run test:e2e` to confirm pass

---

## Phase 8: Polish & Deployment (2 tasks) ✅ COMPLETE

**Goal**: Production deployment

- [X] T037 [P] Add `frontend/src/css/custom.css` with tier colors (green=A, blue=B, purple=C)
- [X] T038 Build and deploy: `npm run build` then deploy to Vercel/Netlify/GitHub Pages

---

## Phase 9: Complete Curriculum Content (P2) (23 tasks)

**Goal**: Complete all remaining chapters (3-10, 12-15, 17-27) to deliver the full 13-week curriculum

**Test**: Learners can complete all 13 weeks of content with comprehensive coverage of ROS 2, Simulation, Navigation, and VLA topics

### Module 1 Completion (8 tasks)

**Week 2: Python & DSP**
- [X] T039 [P] Generate `frontend/docs/module-1/week-2/ch03-python-patterns.mdx` (OOP for ROS 2, NumPy arrays, async patterns)
- [X] T040 [P] Generate `frontend/docs/module-1/week-2/ch04-dsp-basics.mdx` (Low-pass filters, Fourier transforms, noise reduction)

**Week 3: Services, Actions & Lifecycle**
- [X] T041 [P] Generate `frontend/docs/module-1/week-3/ch05-ros2-services-actions.mdx` (Request-response vs streams, action servers, feedback)
- [X] T042 [P] Generate `frontend/docs/module-1/week-3/ch06-lifecycle-nodes.mdx` (Managed node states, error handling, graceful degradation)

**Week 4: Transforms & Robot Models**
- [X] T043 [P] Generate `frontend/docs/module-1/week-4/ch07-tf2-transforms.mdx` (Coordinate frames, transform trees, base_link/odom/map)
- [X] T044 [P] Generate `frontend/docs/module-1/week-4/ch08-urdf-robot-models.mdx` (URDF syntax, links/joints, robot_state_publisher)

**Week 5: Testing & CI/CD**
- [X] T045 [P] Generate `frontend/docs/module-1/week-5/ch09-unit-testing-pytest.mdx` (pytest fixtures for ROS 2, mocking nodes)
- [X] T046 [P] Generate `frontend/docs/module-1/week-5/ch10-launch-testing.mdx` (Integration tests, launch testing, GitHub Actions CI)

### Module 2 Completion (4 tasks)

**Week 6: Gazebo & Sensor Simulation**
- [X] T047 [P] Generate `frontend/docs/module-2/week-6/ch12-simulating-sensors.mdx` (LiDAR/camera/IMU plugins, sensor noise models)

**Week 7: Isaac Sim & Sim2Real**
- [X] T048 [P] Generate `frontend/docs/module-2/week-7/ch13-isaac-sim-essentials.mdx` (Omniverse, PhysX, USD assets, URDF import)
- [X] T049 [P] Generate `frontend/docs/module-2/week-7/ch14-gpu-physics-rendering.mdx` (RTX rendering, GPU-accelerated physics, faster-than-real-time)
- [X] T050 [P] Generate `frontend/docs/module-2/week-7/ch15-domain-randomization.mdx` (Sim2real transfer, texture/lighting/physics randomization)

### Module 3 Completion (7 tasks)

**Week 8: Nav2 Architecture**
- [X] T051 [P] Generate `frontend/docs/module-3/week-8/ch17-nav2-stack-overview.mdx` (Behavior trees, global/local planners, costmaps, recovery behaviors)

**Week 9: SLAM Algorithms**
- [X] T052 [P] Generate `frontend/docs/module-3/week-9/ch18-slam-fundamentals.mdx` (EKF-SLAM, Graph-SLAM, loop closure concepts)
- [X] T053 [P] Generate `frontend/docs/module-3/week-9/ch19-gmapping-cartographer.mdx` (GMapping 2D SLAM, Cartographer with loop closure)
- [X] T054 [P] Generate `frontend/docs/module-3/week-9/ch20-rtab-map.mdx` (RGB-D SLAM with Intel RealSense, map_server, AMCL localization)

**Week 10: Visual SLAM & Voice Navigation**
- [X] T055 [P] Generate `frontend/docs/module-3/week-10/ch21-vslam-orb-slam.mdx` (ORB-SLAM3, monocular/stereo/RGB-D SLAM)
- [X] T056 [P] Generate `frontend/docs/module-3/week-10/ch22-sensor-fusion-vio.mdx` (Visual-Inertial Odometry, camera + IMU fusion)
- [X] T057 [P] Generate `frontend/docs/module-3/week-10/ch23-voice-to-navigation.mdx` (Whisper/Vosk speech recognition, NLP to Nav2 waypoints)

### Module 4 Completion (4 tasks)

**Week 11: VLA Architecture & Transformers**
- [ ] T058 [P] Generate `frontend/docs/module-4/week-11/ch24-vla-paradigm.mdx` (Vision-Language-Action architecture, multimodal transformers)
- [ ] T059 [P] Generate `frontend/docs/module-4/week-11/ch25-transformer-architecture.mdx` (CLIP vision encoder, Llama/Phi language decoder, attention mechanisms)
- [ ] T060 [P] Generate `frontend/docs/module-4/week-11/ch26-openvla-rt2.mdx` (OpenVLA model architecture, RT-2 deep dive, imitation learning)

**Week 12: Fine-Tuning & Action Spaces**
- [ ] T061 [P] Generate `frontend/docs/module-4/week-12/ch27-fine-tuning-vla.mdx` (LoRA fine-tuning, data collection, action tokenization, safety constraints)

---

## Dependencies & Execution Order

### Critical Path
1. Phase 1 (Setup) → MUST complete before all others
2. Phase 2 (Components) → MUST complete before Phase 3-6 (content needs components)
3. Phase 3 (US1) → SHOULD complete before Phase 4 (need chapters to add quizzes)

### Independent Phases (can run in parallel after Phase 2)
- Phase 5 (US2) and Phase 6 (US3) can run independently
- Phase 7 (Validation) can start after Phase 2 (validators don't need content)

### Parallelization Opportunities

**Phase 2**: All 6 component tasks (T005-T010) parallel
**Phase 3**: Module index creation (T012, T015, T017, T019) parallel
**Phase 4**: Validation script + glossary (T021, T025) parallel
**Phase 5**: All Tier B tasks (T026-T028) parallel
**Phase 6**: All Tier C tasks (T030-T031) parallel
**Phase 7**: All validators (T033-T035) parallel
**Phase 9**: All 23 chapter generation tasks (T039-T061) can run in parallel - highly parallelizable using Curriculum Architect + Technical Writer agents

---

## Task Summary

**Total Tasks**: 61
**Setup**: 4
**Foundational**: 6
**User Story 1 (P1)**: 10
**User Story 4 (P1)**: 5
**User Story 2 (P2)**: 4
**User Story 3 (P3)**: 3
**Validation**: 4
**Polish**: 2
**Complete Curriculum (P2)**: 23

**MVP (Phase 1-8)**: 38 tasks (62%)
**Full Curriculum (Phase 1-9)**: 61 tasks (100%)
**Completed**: 53 tasks (87%)
**Remaining**: 8 tasks (13%)
**Parallelizable**: 47 tasks (77%)

---

## Independent Test Criteria

### US1 (Complete Beginner Path)
- ✅ Laptop-only learner navigates all 4 modules
- ✅ All chapters render with diagrams and exercises
- ✅ No GPU or hardware blockers present
- ✅ Capstone conceptual design completable

### US4 (Pedagogical Scaffolding)
- ✅ All chapters have prerequisites and learning outcomes
- ✅ Quizzes validate understanding (70% pass threshold)
- ✅ Learner can self-assess readiness before progressing

### US2 (Edge AI Path)
- ✅ Jetson developer deploys 3+ examples on edge hardware
- ✅ Real sensor integration working (camera, LiDAR, IMU)
- ✅ Safety admonitions present before hardware instructions

### US3 (Physical Robot Path)
- ✅ Researcher deploys VSLAM on Unitree
- ✅ Voice-to-navigation pipeline functional on physical robot
- ✅ Dead Man Switch patterns implemented in motor control

---

## Format Validation

✅ All tasks follow `- [ ] [TaskID] [P?] [Story?] Description with file path`
✅ User story tasks labeled ([US1], [US2], [US3], [US4])
✅ Parallelizable tasks marked [P]
✅ File paths specified where applicable
✅ MVP scope clearly identified (Phase 1-3)
