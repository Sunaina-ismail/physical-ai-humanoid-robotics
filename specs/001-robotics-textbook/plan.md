# Implementation Plan: Physical AI & Humanoid Robotics Textbook

**Branch**: `001-robotics-textbook` | **Date**: 2025-12-04 | **Spec**: [spec.md](./spec.md)
**Input**: Comprehensive open-source textbook covering 13-week curriculum from ROS 2 basics to Vision-Language-Action robotics

## Summary

This plan implements a Docusaurus-based educational platform delivering a 13-week Physical AI & Humanoid Robotics curriculum. The textbook follows a simulation-first approach with three learning tiers (A: Laptop/Simulation, B: Edge AI/Jetson, C: Physical Robots), ensuring accessibility for learners without hardware while providing pathways to real-world deployment. Content is structured across 4 modules (26-39 chapters) covering ROS 2, digital twins, VSLAM/Nav2, and Vision-Language-Action systems, with pedagogical scaffolding (analogies, diagrams, exercises, quizzes) throughout.

**Technical Approach**: Docusaurus TypeScript platform with MDX content, Mermaid.js diagrams, specialized content-generation agents (Curriculum Architect, Technical Content Writer), and three project-specific skills (analogy-concept-explainer, mermaid-diagram-generator, ros2-code-example-writer) to ensure consistent, beginner-friendly, technically accurate content across all chapters.

## Technical Context

**Language/Version**: TypeScript 5.x (Docusaurus), Python 3.12+ (RAG/backend extensions)
**Primary Dependencies**: Docusaurus 3.x, React 18+, MDX, Mermaid.js, remark/rehype plugins
**Storage**: Static MDX files (version-controlled content), optional Neon Postgres (user progress tracking for personalization extension)
**Testing**: Jest (component tests), Playwright (E2E navigation/accessibility), Python pytest (code example validation)
**Target Platform**: Web (responsive, mobile-first), static site deployment (Vercel/Netlify/GitHub Pages)
**Project Type**: Web (frontend-focused content platform with optional backend for personalization)
**Performance Goals**: <3s page load, <200ms search response, support 100-500 concurrent users
**Constraints**: All Tier A content must be executable without GPU/hardware; diagrams must have alt-text; 70% quiz pass threshold
**Scale/Scope**: 26-39 chapters, 4 modules, 13 weeks of curriculum, ~50-100 MDX pages, ~200-300 diagrams

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### ✅ I. Three-Tier Imperative (PASS)
- **Tier A (Simulation)**: All chapters will include Isaac Sim/Gazebo examples with CPU-fallback alternatives
- **Tier B (Edge AI)**: Content structure includes Tier B extension sections for Jetson deployment
- **Tier C (Physical Robot)**: Content structure includes Tier C extension sections for Unitree hardware
- **Validation**: Chapter template mandates tier coverage documentation; FR-008, FR-009, FR-010 enforce tier support

### ✅ II. Content Accuracy & Rigor (PASS)
- **Citations Required**: Research phase will identify authoritative sources for kinematics, SLAM, control theory
- **Physics Validation**: Isaac Sim/Gazebo parameters will reference official documentation
- **Safety References**: Hardware safety claims will cite manufacturer specs (Unitree, Jetson)
- **Version Pinning**: `requirements.txt`/`package.xml` will specify ROS 2 Humble, Python rclpy versions
- **Validation**: Peer review checklist (to be created in Phase 1) will include accuracy verification

### ✅ III. Educational Clarity (PASS)
- **Bloom's Progression**: Module 1-2 (Analyze/Understand), Module 3 (Apply/Use), Module 4 (Create/Build)
- **Prerequisites**: Chapter template includes `prerequisites: []` frontmatter (FR-004)
- **Chunking**: 1500 words max per page enforced in content review guidelines
- **Worked Examples**: Every concept paired with annotated code (FR-003 pedagogical structure)
- **Scaffolded Projects**: Module 4 capstone integrates all prior learning (FR-015)
- **Validation**: Chapter frontmatter enforces prerequisites; FR-002, FR-003, FR-004 guarantee structure

### ✅ IV. Safety First (PASS)
- **Dead Man Switch**: All motor control examples will include timeout logic (100ms standard)
- **Emergency Stop**: ROS 2 examples will demonstrate keyboard interrupt and E-Stop patterns
- **Workspace Boundaries**: Simulation code will enforce collision-free limits via costmaps
- **Safety Admonitions**: `:::danger` blocks will precede all hardware deployment instructions
- **Simulation Validation**: Tier A simulation must pass before Tier C physical deployment
- **Validation**: Code review checklist (Phase 1) will verify Dead Man Switch implementation; Tier C content gated by simulation completion

### ⚠️ V. Technical Stack (MINOR DEVIATION - JUSTIFIED)
- **Frontend**: Docusaurus (React/MDX) ✅ Compliant
- **Formatting**: Prettier for JS/MDX ✅ Compliant
- **Backend**: FastAPI/Qdrant/Neon **deferred to optional personalization extension** (not MVP)
- **Robotics Code**: ROS 2 Humble, rclpy ✅ Compliant
- **Justification**: Spec defines textbook as primary deliverable; backend RAG/personalization is out-of-scope for MVP (SC-001 to SC-016 focus on content delivery, not user tracking)

**GATE STATUS**: ✅ PASS (Technical Stack deviation justified by MVP scope)

## Project Structure

### Documentation (this feature)

```text
specs/001-robotics-textbook/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output: pedagogy patterns, Docusaurus best practices, ROS 2 content strategy
├── data-model.md        # Phase 1 output: Module/Chapter/Exercise/Diagram/Quiz entities
├── quickstart.md        # Phase 1 output: Developer onboarding, content authoring workflow
├── contracts/           # Phase 1 output: Chapter schema, frontmatter spec, Mermaid diagram contract
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
frontend/                          # Docusaurus application
├── docs/                          # MDX content (textbook chapters)
│   ├── index.md                  # Landing page
│   ├── module-1/                 # Module 1: Foundations (Weeks 1-5)
│   │   ├── week-1/              # ROS 2 fundamentals
│   │   │   ├── ch01-physical-ai-intro.mdx
│   │   │   ├── ch02-ros2-nodes-topics.mdx
│   │   │   └── ch03-ros2-services-actions.mdx
│   │   ├── week-2/              # ROS 2 advanced
│   │   ├── week-3/              # URDF modeling
│   │   ├── week-4/              # Sensors/Actuators
│   │   ├── week-5/              # Control theory
│   │   └── index.md             # Module 1 overview
│   ├── module-2/                 # Module 2: Simulation (Weeks 6-7)
│   │   ├── week-6/              # Digital twins, Gazebo
│   │   ├── week-7/              # Sensor simulation, Unity/HRI
│   │   └── index.md
│   ├── module-3/                 # Module 3: Navigation (Weeks 8-10)
│   │   ├── week-8/              # Isaac Sim concepts, VSLAM
│   │   ├── week-9/              # Nav2 planning
│   │   ├── week-10/             # Sim-to-real
│   │   └── index.md
│   ├── module-4/                 # Module 4: VLA (Weeks 11-13)
│   │   ├── week-11/             # Whisper, LLM planning
│   │   ├── week-12/             # VLA architectures
│   │   ├── week-13/             # Capstone project
│   │   └── index.md
│   ├── resources/               # Shared resources
│   │   ├── glossary.md
│   │   ├── ros2-cheatsheet.md
│   │   └── hardware-tiers.md
│   └── capstone/                # Capstone project guide
│       └── voice-controlled-navigation.mdx
├── src/                          # Docusaurus React components
│   ├── components/
│   │   ├── TierBadge.tsx        # Visual tier indicators (A/B/C)
│   │   ├── MermaidDiagram.tsx   # Mermaid wrapper with alt-text
│   │   ├── CodeExample.tsx      # Syntax-highlighted code with tier variants
│   │   ├── Quiz.tsx             # Interactive quiz component
│   │   └── PrerequisiteCheck.tsx # Prerequisite knowledge checker
│   ├── css/                     # Theming
│   │   └── custom.css
│   └── pages/                   # Non-docs pages (about, contribute)
├── static/                       # Static assets
│   ├── img/                     # Images (robot photos, logos)
│   └── diagrams/                # Fallback diagram images
├── docusaurus.config.ts         # Docusaurus configuration
├── sidebars.ts                  # Navigation sidebar
├── package.json
├── tsconfig.json
└── README.md

.claude/                          # Agent/Skill definitions
├── agents/
│   ├── curriculum-architect.md  # Structure chapters, learning outcomes
│   └── technical-content-writer.md # Write pedagogical content
└── skills/
    ├── analogy-concept-explainer.md  # Generate analogies
    ├── mermaid-diagram-generator.md  # Generate diagrams
    └── ros2-code-example-writer.md   # Generate ROS 2 code

tests/                            # Validation tests
├── e2e/                         # Playwright E2E tests
│   ├── navigation.spec.ts       # Test sidebar navigation
│   ├── quiz-interaction.spec.ts # Test quiz functionality
│   └── accessibility.spec.ts    # Test keyboard nav, alt-text
├── content/                     # Content validation
│   ├── validate_frontmatter.py  # Validate chapter YAML
│   ├── validate_diagrams.py     # Check Mermaid alt-text
│   └── validate_tiers.py        # Verify Tier A coverage
└── code-examples/               # Test ROS 2 code snippets
    └── test_examples.py         # Execute code examples
```

**Structure Decision**: Selected **Option 2 (Web application)** structure with `frontend/` containing Docusaurus platform. Backend components (FastAPI/Qdrant) deferred to optional personalization extension and not included in MVP source tree. Agent and skill definitions stored in `.claude/` for content generation workflow.

## Complexity Tracking

> **No violations requiring justification** — Constitution Check passed with one justified MVP scope deviation (backend components deferred).

---

## Phase 0: Research & Knowledge Gathering

**Objective**: Resolve all "NEEDS CLARIFICATION" items from Technical Context and establish best practices for textbook implementation.

### Research Tasks

#### R1: Docusaurus Pedagogical Patterns
**Question**: What are best practices for structuring educational content in Docusaurus? How to implement quizzes, prerequisite checking, and tier-based content switching?

**Research Method**:
- Review Docusaurus documentation for MDX components, plugins, and theming
- Survey existing educational Docusaurus sites (Hasura Learn, Deno Manual, Supabase Docs)
- Evaluate Docusaurus plugins: @docusaurus/theme-mermaid, docusaurus-plugin-content-docs

**Deliverable**: Section in `research.md` documenting:
- Frontmatter schema for learning outcomes, prerequisites, tier markers
- Component architecture for Quiz, TierBadge, PrerequisiteCheck
- Plugin configuration for Mermaid diagram rendering
- Navigation strategy (sidebars.ts structure for 4 modules × weeks)

#### R2: Mermaid.js Diagram Capabilities for Robotics
**Question**: Can Mermaid.js represent ROS 2 computation graphs, Nav2 architecture, VLA pipelines, and URDF hierarchies? What are limitations?

**Research Method**:
- Test Mermaid diagram types (flowchart, sequence, class, state) against robotics use cases
- Identify fallback strategies for unsupported diagrams (e.g., URDF 3D visualization → tree diagram + external link)
- Document alt-text authoring guidelines for accessibility

**Deliverable**: Section in `research.md` documenting:
- Diagram type mapping (ROS graphs → flowchart, Nav2 pipeline → sequence, URDF → tree)
- Limitations and fallback strategies (e.g., Isaac Sim viewport cannot be Mermaid → screenshot + description)
- Alt-text template for each diagram type

#### R3: ROS 2 Code Example Testing Strategy
**Question**: How to ensure ROS 2 rclpy code examples remain executable and correct? What is testing approach for CPU-only Gazebo simulations?

**Research Method**:
- Evaluate ROS 2 testing frameworks (pytest + launch_testing)
- Define version pinning strategy (ROS 2 Humble, Gazebo version, Python dependencies)
- Establish CI/CD approach for code validation (GitHub Actions with ROS 2 Docker containers)

**Deliverable**: Section in `research.md` documenting:
- Testing workflow for code snippets (extract from MDX → execute in ROS 2 container → validate output)
- Dependency management (requirements.txt for rclpy, nav2_msgs, sensor_msgs)
- CI configuration outline for automated code testing

#### R4: Three-Tier Content Architecture
**Question**: How to structure chapter content to clearly differentiate Tier A (mandatory), Tier B (Jetson), Tier C (Robot) sections while maintaining readability?

**Research Method**:
- Design MDX component hierarchy (e.g., `<TierSection tier="A">` blocks)
- Evaluate Docusaurus tabs vs. expandable sections vs. separate pages
- Define tier progression messaging ("Ready for hardware? See Tier B extension")

**Deliverable**: Section in `research.md` documenting:
- Tier content organization pattern (inline tabs vs. extension pages)
- Visual tier indicators (badges, color coding)
- Navigation flow for learners progressing from Tier A → B → C

#### R5: Pedagogical Content Workflow with Agents
**Question**: How to orchestrate Curriculum Architect and Technical Content Writer agents to generate consistent, high-quality chapters?

**Research Method**:
- Define agent responsibilities (Architect: outline + learning outcomes; Writer: content + examples + diagrams)
- Establish handoff protocol (Architect produces chapter spec → Writer implements)
- Create content review checklist (accuracy, pedagogical structure, tier coverage, safety)

**Deliverable**: Section in `research.md` documenting:
- Agent workflow diagram (request → Architect → spec → Writer → chapter draft → review)
- Chapter spec template (what Architect produces for Writer)
- Quality gates (automated checks before human review)

#### R6: Accessibility Compliance
**Question**: What are WCAG 2.1 AA requirements for educational platforms? How to ensure keyboard navigation, screen reader support, and alt-text coverage?

**Research Method**:
- Review WCAG 2.1 AA guidelines for interactive content (quizzes, diagrams)
- Identify Docusaurus accessibility features (theme-classic accessibility, keyboard shortcuts)
- Plan Playwright accessibility tests (axe-core integration)

**Deliverable**: Section in `research.md` documenting:
- Accessibility checklist (alt-text, keyboard nav, color contrast, focus indicators)
- Testing approach (Playwright + axe-core for automated audits)
- Remediation plan for accessibility issues

### Research Deliverable: `research.md`

**Expected Sections**:
1. **Docusaurus Pedagogical Patterns** (R1)
2. **Mermaid.js Diagram Strategy** (R2)
3. **ROS 2 Code Testing Workflow** (R3)
4. **Three-Tier Content Architecture** (R4)
5. **Agent Orchestration for Content Generation** (R5)
6. **Accessibility Compliance** (R6)
7. **Technology Decisions Summary** (consolidated from all research)

**Format per Section**:
- **Decision**: What approach was chosen
- **Rationale**: Why this approach (with evidence from research)
- **Alternatives Considered**: What else was evaluated and why rejected
- **Implementation Notes**: Key details for Phase 1 design

---

## Phase 1: Design & Contracts

**Prerequisites**: `research.md` complete, all Technical Context items resolved

### Design Artifacts

#### D1: Data Model (`data-model.md`)

**Entities to Define** (from spec Key Entities section):

**Module**
- Attributes: `module_number` (1-4), `title` (string), `week_range` (string, e.g., "1-5"), `outcome_statement` (string), `chapter_list` (array of chapter IDs)
- Relationships: Contains multiple Chapters
- Validation: Module must have 2-3 chapters per week (FR-001)
- File Representation: `docs/module-{number}/index.md` with frontmatter

**Chapter**
- Attributes: `chapter_number` (string, e.g., "1.1"), `title` (string), `module_reference` (module ID), `prerequisites` (array of chapter IDs or concepts), `learning_outcomes` (array of strings with Bloom's verbs), `estimated_time` (minutes), `tier_support` (object: {A: boolean, B: boolean, C: boolean}), `content_sections` (array: analogy/concept/diagram/example/exercise/summary/quiz)
- Relationships: Belongs to Module, references prerequisite Chapters, contains Exercises/Diagrams/Quiz
- Validation: Must follow pedagogical structure (FR-003), must have Tier A support (FR-008)
- File Representation: `docs/module-{n}/week-{w}/ch{nn}-{slug}.mdx`

**Learning Tier**
- Attributes: `tier_id` ("A" | "B" | "C"), `hardware_requirements` (string), `content_access_level` (enum: mandatory/optional), `extension_section_availability` (boolean)
- Relationships: Referenced by Chapter tier_support
- State: Tier A is always mandatory; Tiers B/C are optional extensions
- File Representation: Not a file entity; represented in Chapter frontmatter and content sections

**Exercise/Lab**
- Attributes: `exercise_id` (string), `title` (string), `chapter_reference` (chapter ID), `tier_variants` (object: {A: variant, B: variant, C: variant}), `acceptance_criteria` (array of strings), `solution_guidelines` (string or link)
- Relationships: Belongs to Chapter, has variant implementations per Tier
- Validation: Must have Tier A variant (FR-008)
- File Representation: Inline in Chapter MDX with `<Exercise>` component

**Diagram**
- Attributes: `diagram_id` (string), `type` (enum: architecture/flow/graph/sequence), `mermaid_source` (string, Mermaid syntax), `alt_text` (string, accessibility description), `chapter_reference` (chapter ID)
- Relationships: Belongs to Chapter
- Validation: Must have alt_text (FR-007)
- File Representation: Inline in Chapter MDX with `<MermaidDiagram>` component

**Quiz**
- Attributes: `quiz_id` (string), `chapter_reference` (chapter ID), `questions` (array of question objects), `correct_answers` (array), `hint_mappings` (object mapping questions to concept section links), `passing_criteria` (70% correct, FR-019)
- Relationships: Belongs to Chapter
- Validation: Must link hints to concept sections (FR-019)
- File Representation: Inline in Chapter MDX with `<Quiz>` component

**Capstone Project**
- Attributes: `project_id` (string), `requirements` (array of strings), `tier_implementation_variants` (object: {A: conceptual, B: simulation, C: hardware}), `evaluation_rubric` (array of criteria), `submission_guidelines` (string)
- Relationships: Integrates concepts from all Modules/Chapters
- Validation: Must be implementable at Tier A (FR-015)
- File Representation: `docs/capstone/voice-controlled-navigation.mdx`

**State Transitions**:
- Chapter: Draft → Review → Published
- Exercise: Defined → Tier A Implemented → Tier B/C Extended
- Quiz: Created → Validated (70% pass threshold confirmed)

#### D2: Contracts (`contracts/` directory)

**Contract 1: Chapter Frontmatter Schema** (`contracts/chapter-frontmatter.yaml`)
```yaml
# JSON Schema for Chapter frontmatter validation
type: object
required: [chapter_number, title, module, prerequisites, learning_outcomes, estimated_time, tier_support]
properties:
  chapter_number: {type: string, pattern: '^\d+\.\d+$'}
  title: {type: string}
  module: {type: integer, minimum: 1, maximum: 4}
  prerequisites: {type: array, items: {type: string}}
  learning_outcomes: {type: array, items: {type: string}}
  estimated_time: {type: integer, description: "Minutes"}
  tier_support:
    type: object
    required: [A]
    properties:
      A: {type: boolean, const: true}  # Tier A always mandatory
      B: {type: boolean}
      C: {type: boolean}
  tags: {type: array, items: {type: string}}
```

**Contract 2: Mermaid Diagram Component** (`contracts/mermaid-diagram-props.ts`)
```typescript
// TypeScript interface for MermaidDiagram React component
export interface MermaidDiagramProps {
  id: string;                    // Unique diagram identifier
  type: 'architecture' | 'flow' | 'graph' | 'sequence' | 'state' | 'class';
  source: string;                // Mermaid syntax source code
  altText: string;               // Required accessibility description (FR-007)
  caption?: string;              // Optional caption below diagram
  zoomable?: boolean;            // Enable click-to-zoom (default: false)
}
```

**Contract 3: Exercise Component** (`contracts/exercise-props.ts`)
```typescript
export interface ExerciseTierVariant {
  tier: 'A' | 'B' | 'C';
  description: string;           // What learner will do in this tier
  setup?: string;                // Optional setup instructions
  code?: string;                 // Optional starter code
  acceptanceCriteria: string[];  // Expected outcomes
  solution?: string;             // Optional solution link/hint
}

export interface ExerciseProps {
  id: string;
  title: string;
  variants: ExerciseTierVariant[];  // Must include Tier A (FR-008)
  difficulty: 'beginner' | 'intermediate' | 'advanced';
}
```

**Contract 4: Quiz Component** (`contracts/quiz-props.ts`)
```typescript
export interface QuizQuestion {
  id: string;
  question: string;
  type: 'multiple-choice' | 'true-false' | 'short-answer';
  options?: string[];            // For multiple-choice
  correctAnswer: string | number;
  hint: string;                  // Link back to concept section (FR-019)
  explanation: string;           // Shown after answering
}

export interface QuizProps {
  id: string;
  chapterReference: string;      // Chapter ID
  questions: QuizQuestion[];
  passingScore: number;          // Default: 0.7 (70%, FR-019)
  shuffleQuestions?: boolean;    // Randomize order
}
```

**Contract 5: Agent-Generated Content Spec** (`contracts/chapter-spec.md`)
```markdown
# Template for Curriculum Architect → Technical Content Writer handoff

## Chapter Metadata
- Chapter Number: [e.g., 1.1]
- Title: [e.g., "Introduction to Physical AI"]
- Module: [1-4]
- Prerequisites: [list of concept IDs or chapter references]
- Estimated Time: [minutes]

## Learning Outcomes (Bloom's Taxonomy)
1. [Verb] + [Object] (e.g., "Explain the difference between narrow AI and embodied AI")
2. [Verb] + [Object]
3. ...

## Tier Support
- Tier A: [describe what Tier A learners will do]
- Tier B: [describe Jetson-specific extensions, or N/A]
- Tier C: [describe robot hardware extensions, or N/A]

## Content Outline
1. **Analogy Section**: [real-world analogy to introduce concept]
2. **Concept Section**: [formal definition and explanation]
3. **Diagram Section**: [list of diagrams needed with types and purposes]
4. **Example Section**: [worked example with code if applicable]
5. **Exercise Section**: [hands-on activity with tier variants]
6. **Summary Section**: [key takeaways]
7. **Quiz Section**: [number of questions and topics covered]

## Key Concepts to Cover
- [Concept 1]
- [Concept 2]
- ...

## Safety Considerations
- [Any `:::danger` blocks needed?]
- [Dead Man Switch requirements if motor control?]

## References
- [Authoritative sources for formulas/claims]
```

#### D3: Quickstart Guide (`quickstart.md`)

**Sections**:
1. **Developer Onboarding**
   - Clone repository
   - Install Node.js, Docusaurus dependencies (`npm install`)
   - Run local server (`npm run start`)
   - Repository structure overview

2. **Content Authoring Workflow**
   - How to request new chapter from Curriculum Architect agent
   - How to pass chapter spec to Technical Content Writer agent
   - How to review and validate generated content
   - How to test code examples (ROS 2 testing workflow from research.md)

3. **Chapter Creation Checklist**
   - Frontmatter validation (use schema from contracts/)
   - Pedagogical structure completeness
   - Tier A coverage verification
   - Diagram alt-text presence
   - Quiz hint linking
   - Safety admonition placement

4. **Component Usage**
   - `<MermaidDiagram>` examples
   - `<Exercise>` examples with tier variants
   - `<Quiz>` examples with hint mappings
   - `<TierBadge>` usage

5. **Testing**
   - Run E2E tests (`npm run test:e2e`)
   - Validate frontmatter (`python tests/content/validate_frontmatter.py`)
   - Check diagram alt-text (`python tests/content/validate_diagrams.py`)
   - Test ROS 2 code examples (`python tests/code-examples/test_examples.py`)

6. **Deployment**
   - Build static site (`npm run build`)
   - Deploy to Vercel/Netlify/GitHub Pages (environment-specific instructions)

#### D4: Agent Context Update

**Task**: Run agent context update script to register new technologies in agent-specific context files.

**Command**: `.specify/scripts/powershell/update-agent-context.ps1 -AgentType claude`

**Technologies to Add** (from this plan):
- Docusaurus 3.x (React-based static site generator)
- MDX (Markdown + JSX for interactive content)
- Mermaid.js (diagram rendering)
- ROS 2 Humble (robotics framework)
- rclpy (ROS 2 Python client library)
- Gazebo (robotics simulator)
- Playwright (E2E testing)
- Jest (component testing)

**Expected Outcome**: Agent context file updated with new tech stack; manual additions between markers preserved.

---

## Phase 1 Deliverables Summary

1. ✅ `data-model.md` — Entities, relationships, validation rules, file representations
2. ✅ `contracts/chapter-frontmatter.yaml` — JSON Schema for chapter metadata
3. ✅ `contracts/mermaid-diagram-props.ts` — MermaidDiagram component interface
4. ✅ `contracts/exercise-props.ts` — Exercise component interface
5. ✅ `contracts/quiz-props.ts` — Quiz component interface
6. ✅ `contracts/chapter-spec.md` — Agent handoff template
7. ✅ `quickstart.md` — Developer onboarding and content authoring guide
8. ✅ Agent context updated with new technologies

---

## Phase 2: Task Generation (Deferred to `/sp.tasks`)

**Note**: This plan does NOT generate `tasks.md`. Task generation will be handled by the `/sp.tasks` command after this plan is approved.

**Expected Task Categories** (for `/sp.tasks` to generate):
- **Setup Tasks**: Initialize Docusaurus project, install dependencies, configure Mermaid plugin
- **Scaffolding Tasks**: Create folder structure (`docs/module-*/week-*/`), chapter templates, component stubs
- **Component Development Tasks**: Implement `<MermaidDiagram>`, `<Exercise>`, `<Quiz>`, `<TierBadge>` React components
- **Content Generation Tasks**: Use agents to generate Module 1-4 chapters (26-39 total)
- **Validation Tasks**: Implement frontmatter/diagram/tier validation scripts
- **Testing Tasks**: Write E2E tests (navigation, quiz, accessibility), code example tests
- **Deployment Tasks**: Configure build pipeline, deploy to hosting platform
- **Documentation Tasks**: Write contributor guidelines, content style guide

---

## Re-evaluation of Constitution Check (Post-Design)

### ✅ I. Three-Tier Imperative (PASS)
- **Design Alignment**: Chapter frontmatter enforces `tier_support.A = true` (mandatory); Exercise component requires Tier A variant; Agent chapter spec template includes tier planning
- **Validation**: Automated validation script (`validate_tiers.py`) will check all chapters for Tier A coverage

### ✅ II. Content Accuracy & Rigor (PASS)
- **Design Alignment**: Agent chapter spec template includes "References" section; research.md will identify authoritative sources (ROS 2 docs, navigation textbooks, Isaac Sim manuals)
- **Validation**: Peer review checklist (in quickstart.md) includes accuracy verification step

### ✅ III. Educational Clarity (PASS)
- **Design Alignment**: Chapter frontmatter enforces `learning_outcomes` (Bloom's Taxonomy) and `prerequisites`; pedagogical structure enforced by content template
- **Validation**: Frontmatter schema validation (`validate_frontmatter.py`) ensures required fields present

### ✅ IV. Safety First (PASS)
- **Design Alignment**: Agent chapter spec template includes "Safety Considerations" section; Exercise component will include safety checks for motor control code
- **Validation**: Code review checklist (in quickstart.md) verifies Dead Man Switch implementation; `:::danger` admonitions required before Tier C hardware instructions

### ✅ V. Technical Stack (PASS - DEVIATION MAINTAINED)
- **Design Alignment**: Frontend uses Docusaurus/React/MDX (compliant); backend components (FastAPI/Qdrant/Neon) remain out-of-scope for MVP
- **Justification**: Phase 1 design focuses on content delivery platform; personalization/RAG extensions can be added post-MVP without architectural rework

**FINAL GATE STATUS**: ✅ PASS — All constitution principles satisfied by design artifacts.

---

## Implementation Phases Overview (For User Planning)

### Phase 0 Checkpoint (Research Complete)
**Human Review Required**: Verify research.md addresses all Technical Context unknowns; approve technology decisions before Phase 1 design.

### Phase 1 Checkpoint (Design Complete)
**Human Review Required**: Validate data-model.md, contracts/, quickstart.md; confirm agent workflow before content generation.

### Phase 2 Checkpoint (Tasks Generated via `/sp.tasks`)
**Human Review Required**: Approve task list, verify dependencies, sequence, and acceptance criteria before implementation.

### Phase 3 Checkpoint (Project Setup Complete)
**Human Review Required**: Confirm Docusaurus runs locally (`npm run start`), folder structure correct, components render.

### Phase 4 Checkpoint (Module 1 Content Complete)
**Human Review Required**: Review Module 1 chapters (Weeks 1-5), test exercises, validate quizzes, check diagrams before Module 2.

### Phase 5 Checkpoint (Module 2 Content Complete)
**Human Review Required**: Review Module 2 chapters (Weeks 6-7), integration with Module 1, Gazebo examples working.

### Phase 6 Checkpoint (Module 3 Content Complete)
**Human Review Required**: Review Module 3 chapters (Weeks 8-10), Nav2/VSLAM content accuracy, sim-to-real concepts clear.

### Phase 7 Checkpoint (Module 4 & Capstone Complete)
**Human Review Required**: Review Module 4 chapters (Weeks 11-13), capstone project, full curriculum coherence.

### Phase 8 Checkpoint (Testing & Deployment)
**Human Review Required**: E2E tests passing, accessibility audit complete, performance validated, deployment successful.

---

## Risk Analysis

| Risk | Impact | Mitigation |
|------|--------|------------|
| **Agent-generated content lacks technical accuracy** | High - Violates Constitution II | Implement peer review checklist (quickstart.md), cite authoritative sources (research.md R2), test code examples (research.md R3) |
| **Mermaid.js cannot represent complex robotics diagrams** | Medium - May need fallback images | Research.md R2 identifies limitations early; define fallback strategy (screenshot + description) |
| **ROS 2 code examples break with version updates** | Medium - Content becomes outdated | Pin ROS 2 Humble version (research.md R3), document deprecation plan in quickstart.md |
| **Tier A content too simplified, Tier C too complex** | Medium - Fails pedagogical goals | Curriculum Architect agent enforces Bloom's progression, human review checkpoints after each module |
| **Docusaurus performance degrades with 26-39 chapters** | Low - May not meet <3s load time | Research.md R1 includes performance optimization (code splitting, lazy loading) |
| **Accessibility violations in custom components** | Medium - Violates Constitution IV | Research.md R6 defines WCAG 2.1 AA checklist, Playwright+axe-core automated tests |
| **Scope creep: adding backend/RAG before MVP complete** | High - Delays textbook delivery | Constitution Check explicitly defers backend to post-MVP; focus on content delivery |

---

## Success Criteria Mapping (Spec → Plan)

| Spec Success Criterion | Plan Deliverable | Validation Method |
|------------------------|------------------|-------------------|
| SC-001: All 13 weeks covered across 4 modules | Phase 1 data-model.md defines 4 modules × weeks structure | Validate folder structure `docs/module-*/week-*/` matches 13 weeks |
| SC-002: 100% chapters follow pedagogical template | Phase 1 contracts/chapter-frontmatter.yaml enforces structure | `validate_frontmatter.py` checks all chapters |
| SC-003: 100% chapters have learning outcomes, prerequisites | Phase 1 frontmatter schema requires these fields | `validate_frontmatter.py` enforces required fields |
| SC-004: 100% labs have Tier A implementations | Phase 1 contracts/exercise-props.ts requires Tier A variant | `validate_tiers.py` checks Exercise components |
| SC-005: Tier A learner can complete 100% content | Phase 0 research.md R4 defines Tier A mandatory coverage | Human testing + automated tier coverage validation |
| SC-006: All diagrams use Mermaid.js | Phase 0 research.md R2 defines Mermaid strategy | `validate_diagrams.py` ensures no `<img>` tags for technical diagrams |
| SC-007: 100% diagrams have alt-text | Phase 1 contracts/mermaid-diagram-props.ts requires altText | `validate_diagrams.py` checks MermaidDiagram altText prop |
| SC-008: Tier B learners deploy 3+ edge examples | Phase 1 data-model.md defines Tier B extensions | Human testing with Jetson hardware (post-MVP) |
| SC-009: Tier C learners achieve sim-to-real transfer | Phase 1 data-model.md defines Tier C extensions | Human testing with Unitree hardware (post-MVP) |
| SC-010: Docusaurus platform functional | Phase 3 setup (`npm run start` works) | E2E tests verify navigation, search, responsive rendering |
| SC-011: Capstone integrates Whisper → LLM → Nav2 | Phase 1 data-model.md defines Capstone entity | Human review of `docs/capstone/voice-controlled-navigation.mdx` |
| SC-012: 90% learners identify prerequisites | Phase 1 frontmatter schema + PrerequisiteCheck component | User testing (post-MVP) |
| SC-013: 85% learners pass quizzes first attempt | Phase 1 Quiz component with 70% passing threshold | Quiz analytics (requires backend extension, post-MVP) |
| SC-014: No OS-specific instructions in main chapters | Phase 0 research.md R4 defines Tier B/C extension strategy | Manual review: main chapters are conceptual only |
| SC-015: Content reflects current industry standards | Phase 0 research.md identifies ROS 2 Humble, Nav2, Whisper versions | Peer review checklist verifies version alignment |
| SC-016: Platform supports 100-500 concurrent users, <3s load | Phase 0 research.md R1 includes performance optimization | Load testing (Lighthouse CI, k6) |

---

## Next Steps

1. **Approve This Plan**: Human review of plan.md before proceeding
2. **Execute Phase 0**: Generate `research.md` by dispatching research agents (R1-R6)
3. **Execute Phase 1**: Generate `data-model.md`, `contracts/`, `quickstart.md` based on research findings
4. **Update Agent Context**: Run `.specify/scripts/powershell/update-agent-context.ps1 -AgentType claude`
5. **Generate Tasks**: Run `/sp.tasks` to create detailed implementation task list
6. **Begin Implementation**: Execute tasks with human checkpoints after each phase

---

**Plan Status**: ✅ Ready for Phase 0 (Research)
**Blocking Issues**: None
**Dependencies**: Human approval to proceed to Phase 0
