---
id: 001
title: Physical AI Robotics Textbook Constitution
stage: constitution
date: 2025-12-04
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: master
user: system
command: /sp.constitution
labels: ["constitution", "governance", "standards", "physical-ai", "robotics", "education"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests:
  - Constitution template validation
  - Dependent template consistency check
---

## Prompt

```text
Project: Physical AI & Humanoid Robotics Textbook

Core Principles:

- I. The Three-Tier Imperative: Content MUST provide paths for Simulation (Tier A - Isaac Sim), Edge AI (Tier B - Jetson), and Physical Robot (Tier C - Unitree). Tier A is mandatory.

- II. Content Accuracy & Rigor: All math/physics formulas must be validated against authoritative sources. No speculative claims about hardware safety.

- III. Educational Clarity: Chapters must progress via Bloom's Taxonomy (Analyze -> Apply -> Create). Prerequisites must be explicit.

- IV. Safety First: "Dead Man Switch" logic is non-negotiable for all motor code. Wrapped in `:::danger`.

Key Standards (Technical & Quality):

- Frontend (Docusaurus):
  - Structure: One concept per page (max 2000 words).
  - Metadata: `title`, `description`, and `sidebar_position` required in frontmatter.
  - Assets: Images in `/static/img/[chapter]/` with Alt Text (Mandatory for accessibility).
  - Localization: No hardcoded strings in React components (Must support Urdu toggle).

- Backend (FastAPI/RAG):
  - Stack: Python 3.12+, Qdrant, Neon Postgres.
  - Error Handling: API returns structured JSON errors; UI degrades gracefully (no crashes).

- Code Quality:
  - Runnable: No pseudocode. Examples must be tested.
  - Dependencies: All snippets must list `package.xml` or `requirements.txt` versions.
  - Formatting: PEP 8 (Python) and Prettier (JS/MDX).

- Auth: Better-Auth is mandatory (capture "Hardware Profile" on signup).

Constraints:

- Visuals: Static images PROHIBITED for architecture. Use Mermaid.js (Graphs, TF Trees).
- Workflow:
  - Step 1: Spec (`/sp.specify`) defines Learning Objectives.
  - Step 2: Plan (`/sp.plan`) outlines Sim-to-Real path.
- Deployment: Content must pass "Build Gates" (No broken links, Lighthouse Score > 90, Spell check passed).

Success Criteria (Definition of Done):

- [ ] Docusaurus build passes without warnings.
- [ ] Three-Tier instructions (Sim/Edge/Real) are complete.
- [ ] Safety patterns (`:::danger`) implemented.
- [ ] Accessibility check passed (Alt text + Semantic Mermaid diagrams).
- [ ] Localization check passed (No hardcoded strings).
- [ ] SEO check passed (Metadata present).
```

## Response snapshot

Created comprehensive constitution v1.0.0 for Physical AI & Humanoid Robotics Textbook project following Spec-Kit Plus methodology.

**Key Deliverables**:
1. **Core Principles (4)**:
   - I. Three-Tier Imperative: Mandatory simulation (Tier A), recommended Edge AI (Tier B) and Physical Robot (Tier C)
   - II. Content Accuracy & Rigor: Verifiable technical content with authoritative source citations
   - III. Educational Clarity: Bloom's Taxonomy progression with explicit prerequisites
   - IV. Safety First: Dead Man Switch patterns and `:::danger` admonitions mandatory

2. **Technical Standards**:
   - Frontend: Docusaurus v3.x, MDX, Tailwind CSS, required frontmatter fields (title, description, sidebar_position, prerequisites, tiers, bloom_level)
   - Backend: FastAPI 0.110+, Qdrant Cloud, Neon Serverless Postgres, OpenAI embeddings/LLMs
   - Code Quality: Executable examples only, pinned dependencies, PEP 8/Prettier formatting
   - Auth: Better-Auth with Hardware Profile collection at signup

3. **Content Standards**:
   - Module structure: 4 modules across 13 weeks (ROS 2, Gazebo/Unity, NVIDIA Isaac, VLA)
   - Visual content: Mermaid.js mandatory for architecture diagrams (no static images)
   - Hardware context: Document all three tiers with cost transparency

4. **Development Workflow**:
   - Spec-Kit Plus methodology: `/sp.specify` → `/sp.plan` → `/sp.tasks` → `/sp.implement` → `/sp.adr`
   - Constitution Check in planning phase
   - Git workflow with conventional commits

5. **Quality Gates**:
   - Build gates: Docusaurus build success, link validation, spell check
   - Three-tier completeness check per chapter
   - Safety pattern verification (automated grep + manual review)
   - Accessibility: Lighthouse ≥90, WCAG 2.1 AA compliance
   - Localization: No hardcoded strings, Urdu translation support
   - SEO: Metadata validation, sitemap generation

6. **Governance**:
   - Constitution supersedes all other practices
   - Amendment process via ADR with semantic versioning
   - Periodic compliance audits (monthly 10% sample)
   - Continuous improvement via user feedback and metrics

## Outcome

- ✅ Impact: Established comprehensive governance framework for Physical AI textbook project covering technical standards, educational quality, safety requirements, and development workflow
- 🧪 Tests: Validated constitution against dependent templates (plan-template.md, spec-template.md, tasks-template.md)
- 📁 Files: Created `.specify/memory/constitution.md` with Sync Impact Report
- 🔁 Next prompts: Create project README, initialize Docusaurus project, define first feature specification
- 🧠 Reflection: Constitution successfully balances educational rigor (Bloom's Taxonomy, prerequisites) with technical safety (Dead Man Switch, safety admonitions) and implementation pragmatism (tiered approach accommodating varied student hardware access)

## Evaluation notes (flywheel)

- Failure modes observed: None during constitution creation; potential risks include overly prescriptive standards limiting creative approaches, three-tier requirement potentially overwhelming for simple concepts
- Graders run and results (PASS/FAIL): PASS - All placeholders filled, no bracketed tokens remaining, semantic versioning rules defined, governance procedures explicit
- Prompt variant (if applicable): N/A (initial constitution)
- Next experiment (smallest change to try): Monitor first chapter creation against constitution to identify overly burdensome requirements or missing guidance
