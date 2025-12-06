<!--
SYNC IMPACT REPORT
==================
Version Change: Template (Initial) → 1.0.0 (First Ratification)
Modified Principles: N/A (Initial creation)
Added Sections:
  - Core Principles (4 principles: Three-Tier Imperative, Content Accuracy & Rigor, Educational Clarity, Safety First)
  - Technical Standards (Frontend/Backend/Code Quality/Auth)
  - Content Standards (Structure/Quality/Hardware Context)
  - Development Workflow (Spec-Kit Plus methodology)
  - Quality Gates (Build/Accessibility/Localization/SEO)
  - Governance
Removed Sections: N/A
Templates Requiring Updates:
  ✅ .specify/templates/plan-template.md - Reviewed, constitution check section aligns
  ✅ .specify/templates/spec-template.md - Reviewed, user stories and requirements align
  ✅ .specify/templates/tasks-template.md - Reviewed, task categorization aligns
  ⚠ README.md - Not present, will need creation with project overview
Follow-up TODOs: None
-->

# Physical AI & Humanoid Robotics Textbook Constitution

## Core Principles

### I. The Three-Tier Imperative

**Principle**: All educational content MUST provide learning paths across three implementation tiers. Tier A (Simulation) is mandatory; Tiers B and C are strongly recommended for comprehensive learning.

**Non-Negotiable Requirements**:
- **Tier A - Simulation (MANDATORY)**: Every concept MUST include NVIDIA Isaac Sim or Gazebo simulation examples with executable code
- **Tier B - Edge AI (MANDATORY FOR CONTENT)**: Provide NVIDIA Jetson Orin deployment instructions for AI perception and control
- **Tier C - Physical Robot (MANDATORY FOR CONTENT)**: Include Unitree (Go2/G1) or equivalent robot hardware integration guidance

**Rationale**: Students learn best through progressive complexity—from safe simulation environments to real hardware. Simulation removes cost barriers and enables rapid iteration. Edge AI bridges the sim-to-real gap. Physical robots demonstrate embodied intelligence in action.

**Validation**:
- Each chapter MUST document which tiers are covered
- Tier A examples MUST be tested and executable
- Missing Tiers B or C MUST be justified in chapter metadata

### II. Content Accuracy & Rigor

**Principle**: Technical content MUST be verifiable, precise, and grounded in authoritative sources. No speculation, especially regarding hardware safety.

**Non-Negotiable Requirements**:
- All mathematical formulas (kinematics, dynamics, SLAM) MUST cite authoritative sources (textbooks, research papers, official documentation)
- Physics simulations MUST use validated parameters (gravity, friction, collision models)
- Hardware safety claims MUST reference manufacturer specifications or safety standards
- Code examples MUST be tested against official SDK versions
- No "probably safe" or "should work" statements in safety-critical sections

**Rationale**: Robotics combines multiple disciplines (physics, AI, control theory) where errors compound. Students trust educational materials; inaccuracies can lead to damaged hardware, failed learning outcomes, or safety incidents.

**Validation**:
- References section MUST cite sources for all formulas and safety claims
- Code examples MUST specify exact SDK/library versions in `requirements.txt` or `package.xml`
- Peer review checklist MUST include accuracy verification

### III. Educational Clarity

**Principle**: Content MUST follow evidence-based pedagogical patterns, progressing learners through Bloom's Taxonomy levels with explicit prerequisites.

**Non-Negotiable Requirements**:
- **Bloom's Progression**: Each module advances from Analyze (understand systems) → Apply (use tools) → Create (build projects)
- **Explicit Prerequisites**: Every chapter MUST list required prior knowledge with links to foundational content
- **One Concept Per Page**: Maximum 1500 words per page; complex topics split into digestible units
- **Worked Examples**: Every concept paired with annotated code examples
- **Scaffolded Projects**: Module-end projects that integrate learned concepts

**Rationale**: Adult learners need structured progression. Bloom's Taxonomy ensures depth over breadth. Explicit prerequisites prevent frustration from knowledge gaps. Chunking improves retention.

**Validation**:
- Chapter frontmatter MUST include `prerequisites: []` array
- Content reviews MUST verify Bloom's level progression
- Student testing (if available) MUST show >80% comprehension on module assessments

### IV. Safety First

**Principle**: All motor control code MUST implement "Dead Man Switch" safety patterns. Safety warnings MUST use Docusaurus `:::danger` admonitions.

**Non-Negotiable Requirements**:
- **Dead Man Switch Logic**: Motor commands MUST time out if not refreshed within defined intervals (e.g., 100ms)
- **Emergency Stop**: All robot control examples MUST include E-Stop mechanisms (keyboard interrupt, hardware button)
- **Workspace Boundaries**: Simulation and physical robot code MUST enforce collision-free workspace limits
- **Safety Admonitions**: Use `:::danger` blocks for warnings about hardware damage, injury risks, or unrecoverable states
- **Testing Before Deployment**: Simulation MUST validate control logic before any physical robot execution

**Rationale**: Humanoid robots have high kinetic energy and can cause injury or equipment damage. Students may lack experience with safety protocols. Educational code is often copied; unsafe examples proliferate quickly.

**Validation**:
- Code reviews MUST verify Dead Man Switch implementation in all motor control snippets
- `:::danger` blocks MUST appear before any physically dangerous operations
- Simulation tests MUST demonstrate E-Stop and timeout behaviors

## Technical Stack & Standards

### Frontend/Content
- **Framework**: Docusaurus (React/MDX)
- **Formatting**: Prettier for JS/MDX
- **Localization**: Content structure must support future Urdu translation toggle

### Backend/RAG
- **Language**: Python 3.12+
- **API Framework**: FastAPI
- **Vector Database**: Qdrant
- **Relational Database**: Neon (Postgres)
- **Formatting**: Ruff/Black for Python

### Robotics Code
- **ROS Version**: ROS 2 (Humble/Jazzy)
- **Python Interface**: `rclpy`
- **Simulation**: NVIDIA Isaac Sim, Gazebo (where appropriate)

### Authentication
- **Framework**: Better-Auth (for personalization bonus feature)

## Governance

### Amendment Procedure
1. Proposed changes documented with rationale
2. Impact analysis on existing content and templates
3. Version bump following semantic versioning:
   - **MAJOR**: Backward incompatible changes, principle removals/redefinitions
   - **MINOR**: New principles added, material expansions
   - **PATCH**: Clarifications, wording fixes, non-semantic refinements
4. Update dependent templates (plan-template.md, spec-template.md, tasks-template.md)
5. Migration plan for existing content if needed

### Compliance Review
- All PRs must verify compliance with Core Principles I-VII
- Technical Stack deviations require documented justification
- Agent Workflow must be followed for all content generation
- Complexity must be justified when introducing new dependencies

### Enforcement
- Constitution supersedes individual preferences
- Template alignment is mandatory (plan, spec, tasks templates must reflect
  constitution)
- Non-compliance blockers must be resolved before merge

---

**Version**: 1.0.0
**Ratified**: 2025-12-04
**Last Amended**: 2025-12-04
**Project**: Physical AI & Humanoid Robotics Textbook (Hackathon Submission)
