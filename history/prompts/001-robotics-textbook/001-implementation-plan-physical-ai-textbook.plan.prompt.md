---
id: 001
title: Implementation Plan for Physical AI Textbook
stage: plan
date: 2025-12-04
surface: agent
model: claude-sonnet-4-5
feature: 001-robotics-textbook
branch: 001-robotics-textbook
user: developer
command: /sp.plan
labels: ["planning", "textbook", "docusaurus", "ros2", "curriculum"]
links:
  spec: specs/001-robotics-textbook/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/001-robotics-textbook/plan.md
tests:
  - N/A (planning phase)
---

## Prompt

Plan the implementation of the "Physical AI & Humanoid Robotics Textbook" using @specs\001-robotics-textbook\spec.md.

Phases:
1. **Project Setup** – In @frontend folder, install Docusaurus (TypeScript). Verify setup with `npm run start`.
2. **Scaffolding** – Create folder structure for the textbook under `/docs`. Add chapter templates with placeholders for learning outcomes, theory, labs, and diagrams. Pause for verification.
3. **Module Writing** – Write modules one by one using subagents:
   - **Curriculum Architect** – structure-chapter, sequencing, learning outcomes
   - **Technical Content Writer** – analogy-concept-explainer, mermaid-diagram-generator, ros2-code-example-writer
   Pause after each module for review and `npm run start` test.
4. **Tier Verification** – Ensure all labs support Tier A (Simulation), Tier B (Jetson), Tier C (Robot).

Technical Requirements:
- Markdown-native content only (`.mdx`)
- Deterministic paths under `/docs`
- All subagents in `/.claude/agents/`
- All skills in `/.claude/skills/`
- Stop after each phase for human checkpoint before continuing

## Response snapshot

Created comprehensive implementation plan for Physical AI & Humanoid Robotics Textbook with the following structure:

**Technical Context**: Docusaurus 3.x (TypeScript), React 18+, MDX, Mermaid.js for diagrams, ROS 2 Humble content, Python 3.12+ for validation scripts. Static content platform targeting 26-39 chapters across 4 modules, 13 weeks of curriculum.

**Constitution Check**: All five principles validated (Three-Tier Imperative, Content Accuracy & Rigor, Educational Clarity, Safety First, Technical Stack). Backend components (FastAPI/Qdrant/Neon) deferred to post-MVP as justified deviation.

**Project Structure**:
- `frontend/` with Docusaurus platform
- `docs/module-{1-4}/week-{1-13}/` chapter hierarchy
- `.claude/agents/` for Curriculum Architect and Technical Content Writer
- `.claude/skills/` for analogy-concept-explainer, mermaid-diagram-generator, ros2-code-example-writer
- `tests/` for E2E (Playwright), content validation (Python scripts), and code example testing

**Phase 0 (Research)**: Six research tasks defined:
1. Docusaurus pedagogical patterns (frontmatter, components, plugins)
2. Mermaid.js diagram capabilities for robotics (ROS graphs, Nav2, VLA)
3. ROS 2 code example testing strategy (pytest, launch_testing, CI/CD)
4. Three-tier content architecture (Tier A mandatory, B/C extensions)
5. Agent orchestration workflow (Architect → Writer handoff)
6. Accessibility compliance (WCAG 2.1 AA, Playwright+axe-core)

**Phase 1 (Design)**: Artifacts to generate:
1. `data-model.md` - Module, Chapter, Exercise, Diagram, Quiz, Capstone entities
2. `contracts/` - Frontmatter schema, component interfaces (TypeScript), agent handoff template
3. `quickstart.md` - Developer onboarding, content authoring workflow, testing, deployment
4. Agent context update with new tech stack

**Phase 2**: Deferred to `/sp.tasks` command (setup, scaffolding, component dev, content generation, validation, testing, deployment tasks)

**Implementation Checkpoints**: 8 human review gates defined:
- Phase 0: Research complete
- Phase 1: Design complete
- Phase 2: Tasks generated
- Phase 3: Project setup
- Phase 4-7: Module 1-4 content complete
- Phase 8: Testing & deployment

**Risk Mitigation**: Identified 7 risks with mitigation strategies (agent content accuracy, Mermaid limitations, ROS version updates, tier complexity balance, performance, accessibility, scope creep)

**Success Criteria Mapping**: All 16 spec success criteria (SC-001 to SC-016) mapped to plan deliverables with validation methods

## Outcome

- ✅ Impact: Comprehensive implementation plan created covering all phases from research to deployment with clear human checkpoints. Constitution-aligned design with Three-Tier Imperative enforced at schema level.
- 🧪 Tests: No tests run (planning phase). Defined test strategy: E2E (Playwright), content validation (Python), accessibility (axe-core), ROS code examples (pytest).
- 📁 Files: Created `specs/001-robotics-textbook/plan.md` (640+ lines)
- 🔁 Next prompts:
  1. Execute Phase 0 research (dispatch 6 research agents to generate `research.md`)
  2. Execute Phase 1 design (generate `data-model.md`, `contracts/`, `quickstart.md`)
  3. Run `/sp.tasks` to generate detailed task list
- 🧠 Reflection: Plan balances pedagogical rigor (Bloom's Taxonomy, prerequisites, scaffolding) with technical complexity (Docusaurus, MDX, Mermaid, ROS 2). Agent workflow (Curriculum Architect → Technical Content Writer) ensures consistent content generation. Critical success factor: maintaining Tier A (simulation-only) accessibility while providing Tier B/C hardware pathways.

## Evaluation notes (flywheel)

- Failure modes observed: None (plan generation successful)
- Graders run and results (PASS/FAIL): Constitution Check PASS (5/5 principles validated)
- Prompt variant (if applicable): Standard `/sp.plan` workflow
- Next experiment (smallest change to try): Dispatch Phase 0 research agents to validate Docusaurus pedagogical patterns and Mermaid robotics diagram capabilities before Phase 1 design
